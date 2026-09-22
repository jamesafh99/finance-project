# Multi-Asset Portfolio Analytics

Python-based quantitative research project for constructing, analysing and optimising a strategic multi-asset portfolio.

The project implements an end-to-end workflow covering market data acquisition, data cleaning, portfolio construction, performance measurement, risk analysis and portfolio optimisation using daily financial data.

## Overview

The portfolio is designed as a **long-only, unlevered portfolio denominated in USD**, with an equal-weight allocation used as the initial baseline.

The investable universe is intentionally small and diversified across different economic exposures:

| Instrument | Exposure | Portfolio role |
|---|---|---|
| `VT` | Global equities | Growth |
| `IEF` | US Treasuries 7–10Y | Recession / disinflation defence |
| `STIP` | US TIPS 0–5Y | Inflation protection |
| `GSG` | Broad commodities | Stagflation / supply-shock exposure |
| `SGOL` | Physical gold | Crisis diversification |

`DGS3MO`, the 3-Month Treasury Constant Maturity Rate from FRED, is used separately as the USD risk-free rate proxy.

The current research period covers **2016–2025** using daily observations.

## Research Workflow

```text
Market data
    ↓
Data cleaning
    ↓
Portfolio construction
    ↓
Performance & risk analysis
    ↓
Portfolio optimisation
```

The workflow is implemented sequentially across the project notebooks:

| Notebook | Purpose |
|---|---|
| `00_data_download.ipynb` | Download and validate market and risk-free data |
| `01_data_cleaning.ipynb` | Clean, align and prepare the analytical dataset |
| `02_portfolio_construction.ipynb` | Construct the baseline portfolio and calculate returns |
| `03_analysis_and_risk.ipynb` | Analyse performance, drawdowns and portfolio risk |
| `04_optimization.ipynb` | Evaluate alternative portfolio allocations |

Reusable logic is kept under `src/` rather than duplicated across notebooks.

## Project Structure

```text
finance-project/
├── data/
│   ├── raw/                    # Downloaded source data (generated locally)
│   └── processed/              # Clean datasets used for analysis
│
├── notebooks/
│   ├── 00_data_download.ipynb
│   ├── 01_data_cleaning.ipynb
│   ├── 02_portfolio_construction.ipynb
│   ├── 03_analysis_and_risk.ipynb
│   └── 04_optimization.ipynb
│
├── src/
│   ├── config.py
│   ├── data_cleaner.py
│   ├── data_downloader.py
│   ├── helpers_io.py
│   └── __init__.py
│
├── reports/
│   └── figures/
│
├── misc/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Quick Start

Clone the repository:

```bash
git clone https://github.com/jamesafh99/finance-project.git
cd finance-project
```

Create a virtual environment:

```bash
python -m venv env-finance-project
```

Activate it on Windows:

```powershell
.\env-finance-project\Scripts\Activate.ps1
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

Create a local `.env` file from the provided example:

```powershell
Copy-Item .env.example .env
```

Then run the notebooks sequentially, starting with:

```text
notebooks/00_data_download.ipynb
```

The first notebook downloads the raw datasets required by the rest of the pipeline.

## Data

Market data for the investable assets are downloaded from **Yahoo Finance** using `yfinance`.

The USD risk-free proxy is obtained from **FRED** using the `DGS3MO` series.

The acquisition pipeline performs basic structural validation before saving the raw datasets, including:

- Required-column checks
- Date validation
- Duplicate-date detection
- Missing-observation checks
- Data-period coverage checks

Raw observations are not silently cleaned during acquisition. Data treatment and alignment are handled separately in `01_data_cleaning.ipynb`.

## Methodology

The project follows a few core design principles:

- The asset universe is defined before portfolio optimisation or performance analysis.
- The baseline portfolio is long-only, unlevered and equally weighted.
- Raw data acquisition is separated from analytical cleaning.
- Portfolio performance is evaluated using both return and risk measures.
- Downside and tail risk are analysed in addition to standard volatility.
- Optimised allocations are evaluated relative to the baseline portfolio rather than in isolation.

The analysis includes metrics such as annualised return, volatility, Sharpe ratio, drawdowns, VaR and CVaR, together with correlation and diversification diagnostics.

## Current Status

The project is currently being rebuilt and validated sequentially.

`00_data_download.ipynb` and `01_data_cleaning.ipynb`, together with their supporting modules, have been refactored and validated against the updated asset universe and FRED risk-free series.

The portfolio construction, risk analysis and optimisation stages are being reviewed before final portfolio results are published here.

## Disclaimer

This project is for research and educational purposes only. It does not constitute investment advice.