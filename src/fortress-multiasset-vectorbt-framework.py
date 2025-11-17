"""
Multi-Asset Strategy Backtester using VectorBT + pandas_ta + YFinance

Outputs:
- reports/<TICKER>_report.html (interactive equity + drawdown chart)
- strategy_summary_clean.csv (summary metrics)
"""

# ==========================================================
# IMPORTS
# ==========================================================
import os
import re
import pandas as pd
import vectorbt as vbt
import pandas_ta as ta
import yfinance as yf

from plotly.subplots import make_subplots
import plotly.graph_objects as go

# ==========================================================
# CONFIG
# ==========================================================
TICKERS = [
    "SPY", "TBT", "YCS", "EUO", "GLD", "SLV", "CPER", "USO",
    "URA", "LIT", "DBA", "EWJ", "MCHI", "XLI", "XLC", "XLF",
    "XLK", "XLY", "XLB", "XLP", "XLV", "XLRE", "XLU", "XLE",
    "GOOG", "META", "NFLX", "GE", "RTX", "CAT", "NVDA", "AAPL",
    "AVGO", "MSFT", "BRK-B", "JPM", "AMZN", "TSLA", "ABBV", "LLY",
    "COST", "WMT", "BTC-USD", "ETH-USD", "XRP-USD", "ADA-USD",
    "SOL-USD", "DOGE-USD", "TRX-USD", "AVAX-USD"
]

START_DATE = "2020-01-01"
INITIAL_CASH = 10_000
COMMISSION = 0.002
SIZE_PERCENT = 1

METRICS = ["total_return", "max_dd", "sharpe_ratio", "sortino_ratio", "calmar_ratio"]

REPORTS_DIR = "reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

# ==========================================================
# HELPER FUNCTIONS
# ==========================================================
def safe_filename(s):
    return re.sub(r"[^\w\-_\. ]", "_", s)

def getportfolio_stats(pf, metrics):
    try:
        s = pf.stats(metrics=metrics)
        return s.to_dict()
    except:
        return {m: None for m in metrics}

def get_first_trade_date(pf):
    try:
        df = pf.trades.records_readable
        if df is None or df.empty:
            return None
        for c in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[c]):
                return df[c].min()
        return None
    except:
        return None


def align_weekly_to_daily(series, daily_index, start):
    aligned = series.reindex(daily_index, method="ffill")
    return aligned.loc[start:]


# ==========================================================
# DATA DOWNLOADERS
# ==========================================================
def download_weekly(ticker):
    df = yf.download(ticker, start=START_DATE, progress=False,multi_level_index=False)
    if df.empty:
        return None

    df = df.rename(columns={c:c.title() for c in df.columns})

    required = {"Open","High","Low","Close","Volume"}
    if not required.issubset(df.columns):
        return None

    weekly = df.resample("W").agg({
        "Open":"first",
        "High":"max",
        "Low":"min",
        "Close":"last",
        "Volume":"sum"
    }).dropna()

    return weekly


# ==========================================================
# STRATEGY BUILDERS
# ==========================================================
def build_weekly_trend_strategy(close, high, low):

    dc = ta.donchian(high=high, low=low, close=close, upper_length=10, lower_length=10)
    upper = dc["DCU_10_10"]

    st = ta.supertrend(high, low, close, length=20, multiplier=1.0)
    st_line = st["SUPERT_20_1.0"]
    st_dir = st["SUPERTd_20_1.0"]

    ema21 = ta.ema(close, length=21)
    ema50 = ta.ema(close, length=50)

    entries = (
        (close > upper.shift(1)) &
        (st_dir == 1) &
        (ema21 > ema50)
    ).fillna(False)

    exits = (
        (close < st_line) &
        (st_dir == -1)
    ).fillna(False)

    pf = vbt.Portfolio.from_signals(
        close, entries, exits,
        init_cash=INITIAL_CASH,
        freq="W",
        size=SIZE_PERCENT,
        fees=COMMISSION,
        size_type="percent"
    )

    return pf, st_dir


def build_daily_volatility_strategies(ticker, weekly_supertrend_dir):

    df = yf.download(ticker, start=START_DATE, progress=False,multi_level_index=False)
    if df.empty:
        return None, None, None, None, None

    df = df.rename(columns={c:c.title() for c in df.columns})
    close = df["Close"]; high = df["High"]; low = df["Low"]

    atr = vbt.IndicatorFactory.from_pandas_ta("atr").run(high, low, close, length=20).atrr
    atr_pct = (atr / close) * 100

    fast = vbt.MA.run(atr_pct, window=6, ewm=True).ma
    slow = vbt.MA.run(atr_pct, window=25, ewm=True).ma

    st_daily = weekly_supertrend_dir.reindex(close.index, method="ffill").fillna(0)

    entries = fast.vbt.crossed_above(slow)
    exits = fast.vbt.crossed_below(slow)

    high_vol = vbt.Portfolio.from_signals(
        close,
        entries & (st_daily == -1),
        exits,
        init_cash=INITIAL_CASH,
        freq="1D",
        fees=COMMISSION,
        size=SIZE_PERCENT,
        size_type="percent"
    )

    low_vol = vbt.Portfolio.from_signals(
        close,
        exits & (st_daily == -1),
        entries,
        init_cash=INITIAL_CASH,
        freq="1D",
        size=SIZE_PERCENT,
        size_type="percent"
    )

    return high_vol, low_vol, close, entries, exits


# ==========================================================
# MAIN LOOP
# ==========================================================
all_results = []

for ticker in TICKERS:

    print(f"\n🚀 Processing {ticker}")

    weekly = download_weekly(ticker)
    if weekly is None:
        continue

    close_w, high_w, low_w = weekly["Close"], weekly["High"], weekly["Low"]

    # Weekly trend
    pf_trend, weekly_dir = build_weekly_trend_strategy(close_w, high_w, low_w)

    # Daily volatility
    high_vol, low_vol, close_d, ent_d, ex_d = build_daily_volatility_strategies(ticker, weekly_dir)
    if close_d is None:
        continue

    # First trade date logic
    first_dates = [
        get_first_trade_date(pf_trend),
        get_first_trade_date(high_vol),
        get_first_trade_date(low_vol)
    ]
    first_dates = [d for d in first_dates if d is not None]
    if not first_dates:
        continue

    start = min(first_dates)

    if start not in close_d.index:
        idxs = close_d.index[close_d.index >= start]
        if len(idxs)==0:
            continue
        start = idxs[0]

    bench_close = close_d.loc[start:]
    benchmark = vbt.Portfolio.from_holding(
        bench_close,
        init_cash=INITIAL_CASH,
        freq="1D"
    )

    # Save stats
    trend_stats = getportfolio_stats(pf_trend, METRICS)
    high_stats = getportfolio_stats(high_vol, METRICS)
    low_stats  = getportfolio_stats(low_vol, METRICS)
    ben_stats  = getportfolio_stats(benchmark, METRICS)

    all_results.append({
        "Ticker": ticker,
        "Trend": trend_stats,
        "High_Vol": high_stats,
        "Low_Vol": low_stats,
        "Benchmark": ben_stats
    })

    # ==========================================================
    # BUILD EQUITY + DRAWOWN FIGURE
    # ==========================================================
    trend_eq = align_weekly_to_daily(pf_trend.value(), close_d.index, start)
    high_eq  = high_vol.value().loc[start:]
    low_eq   = low_vol.value().loc[start:]
    ben_eq   = benchmark.value().loc[start:]

    df_equity = pd.DataFrame({
        "Trend": trend_eq,
        "High Vol": high_eq,
        "Low Vol": low_eq,
        "Benchmark": ben_eq
    }).ffill().bfill()

    df_dd = pd.DataFrame({
        "Trend": align_weekly_to_daily(pf_trend.drawdown(), close_d.index, start),
        "High Vol": high_vol.drawdown().loc[start:],
        "Low Vol": low_vol.drawdown().loc[start:],
        "Benchmark": benchmark.drawdown().loc[start:]
    }).reindex(df_equity.index).fillna(0)

    # Plot
    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True,
        row_heights=[0.67, 0.33], vertical_spacing=0.07,
        subplot_titles=(f"{ticker} — Equity Curves", "Drawdowns")
    )

    colors = {
        "Trend": "#2ba0f4",
        "High Vol": "#fa943b",
        "Low Vol": "#42f742",
        "Benchmark": "#f03e3e"
    }

    for col in df_equity.columns:
        fig.add_trace(
            go.Scatter(x=df_equity.index, y=df_equity[col],
                       name=col, mode="lines",
                       line=dict(color=colors[col])),
            row=1, col=1
        )

    for col in df_dd.columns:
        fig.add_trace(
            go.Scatter(x=df_dd.index, y=df_dd[col],
                       name=col, mode="lines",
                       line=dict(color=colors[col]),
                       showlegend=False),
            row=2, col=1
        )

    fig.update_layout(
        template="plotly_dark",
        height=800,
        hovermode="x unified",
        title_text=f"{ticker} Strategy Report",
        margin=dict(l=60, r=60, t=60, b=60)
    )

    fig.update_yaxes(title="Portfolio Value ($)", row=1,col=1)
    fig.update_yaxes(title="Drawdown", tickformat=".0%", row=2,col=1)
    fig.update_xaxes(title="Date", row=2,col=1)

    out = os.path.join(REPORTS_DIR, f"{safe_filename(ticker)}_report.html")
    fig.write_html(out, include_plotlyjs="cdn")

    print(f"✅ Saved: {out}")


# ==========================================================
# SUMMARY TABLE
# ==========================================================
rows = []
for r in all_results:
    t = r["Ticker"]
    for strat in ["Trend", "High_Vol", "Low_Vol", "Benchmark"]:
        d = {"Ticker": t, "Strategy": strat}
        d.update(r[strat])
        rows.append(d)

df_summary = pd.DataFrame(rows)
df_summary.to_csv("strategy_summary_clean.csv", index=False)

print("\n📊 Saved summary → strategy_summary_clean.csv\n")
