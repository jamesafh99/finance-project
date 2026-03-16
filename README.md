# Portfolio Risk & Return Analytics – Mixed Asset Portfolio (2019–2024)

This project implements an end-to-end Python pipeline to analyse the **risk–return profile of a diversified, mixed-asset portfolio** using daily data.  
It covers data acquisition, cleaning, portfolio construction, performance measurement, and advanced risk analytics, with later phases focused on optimisation and reporting.

The work is organised into clearly defined **analytical phases**, designed to be transparent, reproducible and extensible, following a professional quantitative research workflow.

---

## 🎯 Central Question & Scope

**Central question**

> How does the return and risk of a simulated mixed-asset portfolio evolve during 2019–2024, and which simple rebalancing adjustments could improve its risk-adjusted efficiency?

**Sub-questions**

1. How did the portfolio and each individual asset perform during 2019–2024?
2. What level of risk did the portfolio assume, as reflected in volatility, drawdowns and tail-risk metrics?
3. Is diversification effective, or is risk concentrated across correlated instruments?
4. How efficient is the portfolio in risk-adjusted terms (Sharpe, CVaR)?
5. Which simple allocation adjustments could plausibly improve efficiency?

The baseline setup is an **equally weighted, long-only, no-leverage portfolio**, used as a neutral benchmark throughout the analysis.

---

## 📊 Asset Universe

The portfolio uses a **small but diversified universe** across major asset classes.  
All prices are expressed in **USD** and downloaded via `yfinance`.

**Equity Index (ETF)**

- `SPY` – S&P 500 ETF

**Fixed Income (ETFs)**

- `IEF` – iShares 7–10 Year US Treasury Bond ETF

**Commodities (ETFs)**

- `GLD` – Gold ETF  
- `USO` – Oil ETF  
- `UNG` – Natural Gas ETF

**FX**

- `EURUSD=X` – EUR/USD  
- `USDJPY=X` – USD/JPY  

**Risk-free rate proxy**

- `^IRX` – 13-week US Treasury Bill yield, used exclusively as a **risk-free rate proxy** (stored separately from price data).

Clean, aligned price data and the risk-free series are stored under:

- `data/processed/asset_universe.csv`
- `data/processed/risk_free.csv`

---

## 🏗️ Project Roadmap

This project follows a structured, end-to-end quantitative research workflow.

---

## **Phase 1 – Problem Definition & Analytical Framework**

- Define central research question and scope  
- Select core KPIs (return, volatility, Sharpe, drawdown, VaR, CVaR)  
- Fix modelling assumptions (daily data, long-only, equal-weight baseline)  
- Design full project roadmap  

---

## **Phase 2 – Asset Universe Selection**

- Construct a diversified multi-asset universe  
- Avoid redundant exposures and excessive correlation  
- Ensure consistent currency denomination (USD)  
- Validate data availability and liquidity  

---

## **Phase 3 – Data Acquisition & Cleaning**

### **3.1 Data Download – `00_data_download.ipynb`**
- Download daily adjusted prices for each asset  
- Save one CSV per instrument  
- Download ^IRX separately as risk-free rate proxy  

### **3.2 Data Cleaning – `01_data_cleaning.ipynb`**
- Align all assets to a common trading calendar  
- Handle missing values and non-trading days  
- Produce a clean, aligned dataset ready for portfolio analysis  

---

## **Phase 4 – Portfolio Construction & Performance Metrics**

Implemented in `02_portfolio_construction.ipynb`.

- Build an equally weighted portfolio  
- Compute daily portfolio returns and equity curve  
- Integrate the risk-free rate and compute excess returns  
- Compute key performance metrics:
  - Total and annualised return  
  - Annualised volatility  
  - Sharpe ratio  
  - Maximum drawdown  

---

## **Phase 5 – Risk Analytics & Diagnostics**

Implemented in `03_analysis_and_risk.ipynb`.

Includes:

- Return distribution diagnostics (skewness, kurtosis)  
- Rolling volatility analysis (30d / 60d / 90d)  
- Drawdown depth and duration analysis  
- Historical and parametric **VaR / CVaR** (Normal and Student-t)  
- Comparison of tail-risk estimates across methods  

This phase establishes a robust baseline for stress testing and optimisation.

---

## **Phase 6 – Portfolio Optimisation & Rebalancing**

Planned in `04_optimization.ipynb`.

- Volatility-scaled and risk-aware allocations  
- Mean–variance optimisation  
- Comparison against equal-weight benchmark  
- Impact on risk-adjusted performance  

---

## **Phase 7 – Reporting & Visualisation**

Planned extensions:

- Correlation and regime visualisation  
- Risk contribution dashboards  
- Lightweight reporting layer (Plotly / Power BI / web app)  

---

## ▶️ Notebook Execution Flow

Recommended execution order:

1. `00_data_download.ipynb`  
2. `01_data_cleaning.ipynb`  
3. `02_portfolio_construction.ipynb`  
4. `03_analysis_and_risk.ipynb`  
5. `04_optimization.ipynb`

---

## ⚙️ Installation & Setup

```bash
git clone <https://github.com/jamesafh99/finance-project>
cd finance-project
pip install -r requirements.txt
```
---

## 🗂️ Repository structure

```text
FINANCE-PROJECT/
│
├─ data/
│  ├─ raw/
│  │  └─ prices/              # One CSV per asset
│  └─ processed/
│     ├─ asset_universe.csv   # Clean aligned prices
│     └─ risk_free.csv        # ^IRX risk-free rate
│
├─ notebooks/
│  ├─ 00_data_download.ipynb
│  ├─ 01_data_cleaning.ipynb
│  ├─ 02_portfolio_construction.ipynb
│  ├─ 03_analysis_and_risk.ipynb
│  └─ 04_optimization.ipynb   # Planned
│
├─ src/
│  ├─ helpers_io.py
│  ├─ config.py
│  └─ __init__.py
│
├─ reports/
├─ dashboards/
│
├─ requirements.txt
├─ .env.example
├─ .gitignore
└─ README.md
```