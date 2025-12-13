# Portfolio Risk & Return Analytics – Mixed Asset Portfolio (2019-2024)

This project builds an end-to-end pipeline in Python to analyse the risk–return profile of a mixed-asset portfolio. It covers data acquisition, cleaning, portfolio construction, performance metrics and (in later phases) risk analytics, optimisation and dashboarding.

The work is structured in clearly defined **phases**, from problem definition to final visualisation, and is designed to be reproducible.

---

## 🎯 Central Question & Scope

**Central question**

> How does the return and risk of a simulated mixed-asset portfolio evolve during 2019-2024, and what simple rebalancing adjustments could improve its risk-adjusted efficiency?

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

# 🏗️ Project Roadmap

This is the **complete** end-to-end design of the entire project.

## **Phase 1 – Problem Definition & Analytical Framework**

- Define central question + sub-questions  
- Establish main KPIs (return, volatility, Sharpe, drawdown, VaR, CVaR)  
- Choose timeline (focus on 2019-2024 performance)  
- Define modelling assumptions (daily data, long-only, equal weights benchmark)  
- Define full project roadmap for Phases 1–7  

---

## **Phase 2 – Asset Universe Selection**

- Select diversified multi-asset universe  
- Ensure cross-asset exposure: equities, indices, FX, commodities, bonds  
- Validate data availability, liquidity, consistency  
- Create `asset_universe.csv` database

---

## **Phase 3 – Environment, Data Acquisition & Cleaning**

### **3.1 Project Environment Setup**
- Create environment, folder structure, `src/`, `data/`, `notebooks/`  
- Configure `.env`, `.gitignore`, requirements  

### **3.2 Data Download – `00_data_download.ipynb`**
- Download daily historical data for every ticker  
- Save one CSV per ticker in `raw_prices/`  
- Add ^IRX as risk-free rate proxy  
- Update `asset_universe.csv`  

### **3.3 Data Cleaning – `01_data_cleaning.ipynb`**
- Align all assets to a common daily calendar  
- Handle missing values, non-trading days  
- Validate and sanity-check series  
- Compute clean simple returns (vectorized with pandas)  
- Produce a clean dataset ready for portfolio-level analysis  

---

## **Phase 4 – Portfolio Construction & Performance Metrics**

Implemented in `02_portfolio_construction.ipynb`.

### **4.1 Portfolio Construction**
- Build long-only, equally-weighted portfolio (weights sum to 1)  
- Compute daily portfolio returns  
- Build portfolio equity curve  

### **4.2 Risk-Free Rate Integration**
- Align ^IRX yield to portfolio dates  
- Convert annual yield → daily risk-free rate using compound scaling  
- Compute daily excess returns  

### **4.3 Performance Metrics**
Full quant-standard KPIs:

- **Total return**  
- **Realised annualised return** (using total return + actual number of days)  
- **Daily and annualised volatility**  
- **Sharpe Ratio:**  
  - Daily Sharpe (mean excess return / std excess return)  
  - Annualised Sharpe (daily × √252)  
- **Maximum Drawdown:**  
  - Rolling peak  
  - Drawdown = equity / peak − 1  
  - Max drawdown as minimum drawdown value  

---

## **Phase 5 – Risk Analytics & Diagnostics**

To be implemented in `03_analysis_and_risk.ipynb`.

Includes:

- Return distribution analysis (skewness, kurtosis, tail behaviour)  
- Correlation analysis across all assets  
- Diversification evaluation  
- Risk concentration & contributions  
- Historical **VaR**, **CVaR**  
- Stress testing (e.g., oil crash events, rate shocks)  

---

## **Phase 6 – Portfolio Optimisation & Rebalancing**

To be implemented in `04_optimization.ipynb`.

Includes:

- Mean-variance analysis  
- Efficient frontier  
- Simple rebalancing rules (periodic, threshold-based)  
- Compare optimised vs baseline portfolio  
- Impact on return, volatility, Sharpe, drawdown  

---

## **Phase 7 – Dashboard & Reporting Layer**

Planned through Power BI, Plotly, or a lightweight web app.

Includes:

- Interactive dashboard for portfolio evolution  
- Risk overview panels (drawdowns, volatility, correlations)  
- Comparison between baseline and optimised allocations  
- Final storytelling/report with insights for decision-makers  

---

# ▶️ Notebook Execution Flow

Recommended execution:

1. `00_data_download.ipynb` – Download raw prices & risk-free rate  
2. `01_data_cleaning.ipynb` – Clean & align all series  
3. `02_portfolio_construction.ipynb` – Build portfolio + KPIs  
4. `03_analysis_and_risk.ipynb` – Risk analytics (planned)  
5. `04_optimization.ipynb` – Optimisation & rebalancing (planned)  

---

# ⚙️ Installation & Setup

```bash
git clone <your-repo-url>
cd FINANCE-PROJECT
pip install -r requirements.txt
```
---

## 🗂️ Structure of the repository

```text
FINANCE-PROJECT/
│
├─ data/
│  └─ raw/
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
```