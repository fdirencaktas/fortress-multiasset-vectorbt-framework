# 📘 **README.md — Multi-Asset Strategy Backtester (VectorBT + pandas_ta + Plotly)**

**Fortress Quant Toolkit – Project #4**

<div align="center">

### **Multi-Asset Strategy Backtester**

**VectorBT • pandas_ta • YFinance • Plotly • Python**
A flexible, cross-timeframe, multi-asset backtesting framework designed for real-world quant research.

</div>

---

## 📌 **Overview**

This project implements a **multi-asset backtesting and reporting system** combining:

* **Weekly trend strategy**
  Donchian breakout + Supertrend + EMA(21/50)
* **Daily volatility strategies**
  ATR % fast/slow EMA crossover
* **Unified benchmark** aligned to the first active trade
* **Automated Plotly HTML reports per ticker**
* **Unified strategy summary table**

This system is built using:

* **VectorBT** → ultra-fast, vectorized backtesting
* **pandas_ta** → indicator generation
* **YFinance** → real market data
* **Plotly** → professional HTML equity reports
* **Python** → full flexibility & extensibility

This project is part of the **Fortress Quant Toolkit**, a growing set of open-source quant tools.

---

## 🚀 **Features**

### ✅ **Multi-Asset Support**

Supports **60+ assets** across:

* US equities
* ETFs
* Sectors
* Commodities
* Crypto

### ✅ **Cross-Timeframe Strategy Logic**

* Weekly trend model drives macro direction
* Daily volatility models trade only within weekly trend bias

### ✅ **Strategies Included**

#### **1. Weekly Trend Strategy**

* Donchian Channel breakout
* Supertrend direction filter
* EMA(21/50) momentum filter
* Weekly portfolio frequency

#### **2. High-Volatility Strategy (Daily)**

* ATR %
* Fast/slow ATR EMA crossover
* Long signals only when **weekly trend = bearish**

#### **3. Low-Volatility Strategy (Daily)**

* Inverse ATR logic

#### **4. Benchmark**

* Buy & Hold starting at *first trade date*

---

## 📊 **Advanced Metrics**

For each ticker and strategy:

* Total Return
* Max Drawdown
* Sharpe Ratio
* Sortino Ratio
* Calmar Ratio

All results exported into:

```
strategy_summary_clean.csv
```

---

## 📈 **Automated Plotly Reports**

For each asset, the system generates:

```
reports/<TICKER>_report.html
```

Each report includes:

* Equity curve comparison (Trend / High Vol / Low Vol / Benchmark)
* Drawdown comparison
* Fully interactive hover & zoom
* Dark mode dashboards (Plotly Dark)

---

## 📁 **Project Outputs**

### **1. Per-Ticker HTML Reports**

Located in:

```
/reports/
```

Each file contains:

* Equity curves
* Drawdowns
* Strategy overlays

### **2. Unified CSV Summary**

Generated at:

```
strategy_summary_clean.csv
```

Clean, flat format with rows for each:

* Ticker
* Strategy
* Metric

---

## 🧠 **Directory Structure**

```
project/
│
├── reports/                                                      # Auto-generated Plotly reports
│   └── <TICKER>_report.html
│
├── strategy_summary_clean.csv                                    # Unified results table
│
├── backtester-multiasset-vectorbt-framework.py                   # Main script
│
└── README.md                                                     # This file
```

---

## 🔧 **How to Run**

### **1. Install Requirements**

```
pip install -r requirements.txt
```

### **2. Run the Backtester**

```
python backtester.py
```

Reports and summary CSV will appear automatically.

---

## 🧱 **Extending the Project**

Add new strategies by extending:

* Weekly logic
* Daily logic
* New volatility models
* ML models or signals
* Alternative benchmarks
* Risk overlays (vol targeting, trailing stops, etc.)

The project is intentionally modular for expansion.

---

## 🏰 **Part of Fortress Quant Toolkit**

This is project **#4** in the **Fortress Quant Toolkit**, a broader collection of tools designed for:

* systematic investing
* multi-asset quant research
* strategy engineering
* high-efficiency backtesting frameworks
