# 🏰 Fortress Multi-Asset Backtester

Advanced Cross-Timeframe Trend & Volatility Strategy Engine
**VectorBT + pandas_ta + Plotly Dashboard**

---

## 📘 Overview

This project implements a **multi-asset, multi-strategy quant research system** using VectorBT, pandas_ta, and Plotly.
It downloads weekly + daily market data, computes trading signals, executes three strategies (Trend, High-Vol, Low-Vol), and generates **interactive equity + drawdown dashboards** for over 60 tickers.

This is a core module of the **Fortress Quant Toolkit**.

---

## ⚙️ Features

### ✅ Multi-Asset Backtesting (60+ assets)

* US equities
* ETFs & sectors
* Commodities
* Cryptocurrencies

### ✅ Cross-Timeframe System

* Weekly trend model (Donchian + Supertrend + EMA21/50)
* Daily ATR-based volatility strategies
* Daily logic filtered by weekly trend direction

### ✅ Automatic Plotly Report Generation

Creates:

```
reports/<TICKER>_report.html
```

Includes:

* Interactive equity curves
* Strategy drawdowns
* Dark theme dashboard

### ✅ Clean Performance Summary

Exports:

```
strategy_summary_clean.csv
```

Metrics:

* Total Return
* Max Drawdown
* Sharpe
* Sortino
* Calmar

### ✅ Modular & Extendable

Easily add:

* New strategies
* More indicators
* Different timeframes
* ML models
* Custom position sizing

---

## 🧠 Tech Stack

**Core:** Python, NumPy, Pandas, VectorBT

**Indicators:** pandas-ta

**Data:** Yahoo Finance (yfinance)

**Visualization:** Plotly (interactive HTML reports)

**Focus Areas:** Multi-Asset Backtesting · Trend Models · Volatility Systems · Systematic Trading

---

## 🖼️ Sample Result

### **Equity Curves**

*(Generated per asset automatically in /reports)*

```
reports/SPY_report.html
reports/BTC-USD_report.html
reports/NVDA_report.html
...
```

### **Drawdowns**

Included in every HTML dashboard.

### **Strategies Included**

* **Trend Strategy (Weekly)**
* **High-Volatility Strategy (Daily)**
* **Low-Volatility Strategy (Daily)**
* **Benchmark Buy & Hold**

---

## 📈 Example CSV Output (strategy_summary_clean.csv)

| Strategy  | Total Return | Max Drawdown | Sharpe | Sortino | Calmar |
| --------- | ------------ | ------------ | ------ | ------- | ------ |
| Trend     | XX%          | XX%          | X.XX   | X.XX    | X.XX   |
| High Vol  | XX%          | XX%          | X.XX   | X.XX    | X.XX   |
| Low Vol   | XX%          | XX%          | X.XX   | X.XX    | X.XX   |
| Benchmark | XX%          | XX%          | X.XX   | X.XX    | X.XX   |

---

## 🚀 Getting Started

### **1️⃣ Install dependencies**

```
pip install -r requirements.txt
```

### **2️⃣ Run the backtester**

```
python src/fortress-multiasset-vectorbt-framework.py
```

### **3️⃣ View results**

* All HTML dashboards → `/reports/`
* Summary metrics → `strategy_summary_clean.csv`

---

## 🏁 Author

**Fikri Direnç Aktaş**
Quant Developer | Systematic Trader
📧 **[Direncak2@gmail.com](mailto:Direncak2@gmail.com)**
🌐 **[[LinkedIn Profile](https://www.linkedin.com/in/direncaktas/)]**

