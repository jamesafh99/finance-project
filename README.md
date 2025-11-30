# Portfolio Risk & Return Analytics – Mixed Asset Portfolio (2019-2024)

This project builds an end-to-end pipeline in Python to analyse the risk–return profile of a mixed-asset portfolio. It covers data acquisition, cleaning, portfolio construction, performance metrics and (in later phases) risk analytics, optimisation and dashboarding.

The work is structured in clearly defined **phases**, from problem definition to final visualisation, and is designed to be reproducible.

---

## 🎯 Central Question & Scope

**Central question**

> How does the return and risk of a simulated mixed-asset portfolio evolve during 2019-2024,
> and what simple rebalancing adjustments could improve its risk-adjusted efficiency?

**Sub-questions**

1. How did the portfolio and each individual asset perform during 2019-2024 in terms of return?
2. What level of risk did the portfolio assume and how is it reflected in volatility, drawdown and other key metrics?
3. Is there true diversification between assets, or is risk concentrated through correlations across instruments?
4. Was the portfolio efficient in risk-adjusted terms (Sharpe, Sortino, etc.)?
5. Is it advisable to rebalance the portfolio, and what simple change in weights would most likely improve its efficiency?

The project is implemented in Python using daily data, with a baseline **equally weighted, long-only, no-leverage** portfolio as the starting point.

---

## 📊 Asset Universe

The portfolio uses a diversified universe across multiple asset classes. Tickers are downloaded via `yfinance` and stored under `data/raw_prices`.

**Equities**

- `MSFT` – Microsoft  
- `AMZN` – Amazon  
- `NVDA` – NVIDIA  
- `ORCL` – Oracle  
- `JPM` – JPMorgan Chase

**Indices**

- `^GSPC` – S&P 500  
- `^IXIC` – Nasdaq Composite  
- `^FTSE` – FTSE 100

**FX**

- `EURUSD=X` → stored as `EURUSD_prices.csv`  
- `GBPUSD=X` → stored as `GBPUSD_prices.csv`  
- `USDJPY=X` → stored as `USDJPY_prices.csv`

**Commodities (front futures)**

- `CL=F` – Crude Oil (WTI)  
- `BZ=F` – Brent  
- `NG=F` – Natural Gas  
- `GC=F` – Gold  
- `SI=F` – Silver

**Fixed Income (proxies via ETFs)**

- `TLT` – Long-term US Treasuries  
- `IEF` – Intermediate-term US Treasuries

**Risk-free rate proxy**

- `^IRX` – 13-week US T-Bill yield, used as **risk-free rate** proxy.

The consolidated universe (including metadata such as ticker, asset class and descriptions)
is stored in:

- `data/processed/asset_universe.csv`

---

## 🏗️ Project Structure

High-level structure of the repository:

```text
FINANCE-PROJECT/
│
├─ data/
│  ├─ raw/
|     └─ prices/    # One CSV per ticker (e.g. MSFT_prices.csv, CL_prices.csv, IRX_prices.csv)
│  └─ processed/
│     └─ asset_universe.csv
│
├─ notebooks/
│  ├─ 00_data_download.ipynb
│  ├─ 01_data_cleaning.ipynb
│  ├─ 02_portfolio_construction.ipynb
│  ├─ 03_analysis_and_risk.ipynb      # Planned / in progress
│  └─ 04_optimization.ipynb           # Planned / in progress
│
├─ src/
│  ├─ analysis/                       # Future analysis utilities (risk, correlations, etc.)
│  ├─ data/                           # Future data handling helpers
│  ├─ features/                       # Future feature engineering (factors, signals)
│  ├─ viz/                            # Visualisation utilities
│  ├─ __init__.py
|  ├─ config.py                       # Central configuration (paths, tickers, date ranges)
|  └─ helpers_io.py                   # IO utilities (reading/writing config, CSVs, etc.)
│
├─ dashboards/                        # Future dashboards (Power BI / web)
├─ reports/                           # Future reports / exports
│                        
├─ requirements.txt
├─ setup.py
├─ .env.example                       # Template for environment variables
├─ .gitignore
└─ README.md