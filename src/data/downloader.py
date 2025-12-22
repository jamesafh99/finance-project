import pandas as pd
import yfinance as yf
import logging
from pathlib import Path
from typing import List, Tuple, Optional, cast
from src.config import PROJECT_ROOT, DATA_RAW_DIR
from src.data.preprocessing import cleaning_ticker

# Logger setup
logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

# Function to parse tickers from 'tickers.txt'
def parse_tickers(filepath: Path) -> List[str]:
    """
    Reads a text file and returns a list of unique, clean tickers.
    Ignores comments (#) and empty lines.
    
    Args:
        filepath (Path): Path to the .txt file containing tickers.
        
    Returns:
        List[str]: Sorted list of unique tickers.
    """

    if not filepath.exists():
        raise FileNotFoundError(f"Configuration file not found at {filepath}")
    
    with open(filepath, "r") as f:
        lines = f.readlines()
    
    tickers = []
    for line in lines:
        # Deleting any comments
        line = line.split("#")[0]

        # Removing blank spaces
        line = line.strip()

        if line:
            tickers.append(line)
    
    unique_tickers = sorted(list(set(tickers)))
    logger.info(f"Loaded {len(unique_tickers)} unique tickers from {filepath.name}")
    return unique_tickers

# Function to deeply analyse the info of each ticker from 'tickers.txt'
def deep_ticker_analysis(user_tickers: List[str], target_currency: str, risk_free_ticker: Optional[str]) -> Tuple[List[str], pd.DataFrame]:
    """
    Analyzes the list, detects currencies, and auto-injects FX pairs (e.g., GBPUSD=X).
    
    Args:
        user_tickers (List[str]): Initial list of tickers.
        target_currency (str): The portfolio's base currency (default: GBP).
        
    Returns:
        Tuple[List[str], pd.DataFrame]: The expanded ticker list and the metadata DataFrame.
    """
    logger.info("Analyzing assets and checking for FX dependencies")

    tickers_list = user_tickers.copy()
    metadata_log = []
    currencies_found = set()

    # Smart addition: Risk Free Rate
    if risk_free_ticker and (risk_free_ticker not in tickers_list):
        logger.info(f"Auto-adding Risk-free Rate ticker: {risk_free_ticker}")
        tickers_list.append(risk_free_ticker)

    for ticker in tickers_list:
        currency = "USD"    # Default assumption
        quote_type = "UNKNOWN"
        asset_name = "UNKNOWN"

        try:
            yf_ticker = yf.Ticker(ticker)
            info = yf_ticker.info
            currency = info.get("currency", "USD").upper()
            quote_type = info.get("quoteType", "EQUITY").upper()
            asset_name = info.get("shortName") or info.get("longName") or ticker

            # Manual override for risk-free rate 
            if risk_free_ticker and (ticker == risk_free_ticker):
                quote_type = "RATE"
                currency = "RATE"
                asset_name = f"Risk-free Rate: {asset_name}"

        except Exception as e:
            logger.warning(f"Metadata fetch failed for {ticker}. Assuming USD. Error {e}")
        
        currencies_found.add(currency)
        metadata_log.append({
            "ticker": ticker,
            "name": asset_name,
            "original_currency": currency,
            "type": quote_type,
            "source": "user_input"
        })

    # FX dependencies
    for curr in currencies_found:
        if curr != target_currency and curr != "RATE" and curr != "UNKNOWN":
            fx_ticker = f"{target_currency}{curr}=X"
        
            if fx_ticker not in tickers_list:
                logger.info(f"FX dependency: {fx_ticker} (for {curr} assets)")
                tickers_list.append(fx_ticker)

                metadata_log.append({
                    "ticker": fx_ticker,
                    "name": f"{target_currency}/{curr} Exchange Rate",
                    "original_currency": curr,
                    "type": "CURRENCY",
                    "source": "FX_dependency"
                })

    return tickers_list, pd.DataFrame(metadata_log)

# Downloading data from Yahoo Finance
def download_data(start_date: str, end_date: str, target_currency: str, risk_free_ticker: Optional[str], input_filename: str = "tickers.txt") -> pd.DataFrame:
    """
    Main execution function for parsing, analyzing, and downloading.
    Dates are MANDATORY to ensure reproducibility of the analysis.
    
    Args:
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
        input_filename (str): Name of the config file in the project root.
        target_currency (str): Base currency for the portfolio.
        
    Returns:
        pd.DataFrame: The metadata summary of downloaded assets.
    """
    logger.info(f"Starting pipeline. Period: {start_date} to {end_date}")

    input_path = PROJECT_ROOT / input_filename

    # 1. Parse input
    try:
        user_tickers = parse_tickers(input_path)
    except FileNotFoundError as e:
        logger.error(str(e))
        return pd.DataFrame()
    
    # 2. Deep tickers analysis
    tickers_list, metadata = deep_ticker_analysis(user_tickers, target_currency=target_currency, risk_free_ticker=risk_free_ticker)

    # 3. Save data manifest
    manifest_path = DATA_RAW_DIR / "data_manifest.csv"
    DATA_RAW_DIR.mkdir(parents=True, exist_ok=True) # Ensure directory exists (Safety check)
    
    metadata.to_csv(manifest_path, index=False)
    logger.info(f"Metadata manifest saved to {manifest_path}")

    # 4. Download engine
    prices_dir = DATA_RAW_DIR / "prices"
    prices_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Starting download for {len(tickers_list)} assets...")

    download_info = {"success": 0, "failed": 0}

    for ticker in tickers_list:
        try:
            # Downloading data
            data = cast(pd.DataFrame, yf.download(ticker, start=start_date, end=end_date, progress=False, auto_adjust=True, multi_level_index=False))

            # Sanity check
            if data.empty:
                logger.warning(f"Skipping {ticker} (No data returned)")
                download_info["failed"] += 1
                continue
            
            # Reset index to have "Date" as a column for better data manipulation
            data = data.reset_index()

            # Clean filename (removing ^, =X, =F from tickers) and full file path
            filename = f"{cleaning_ticker(ticker)}_prices.csv"
            filepath = prices_dir / filename

            # Save as CSV in data/raw/prices
            data.to_csv(filepath, index=False)
            download_info["success"] += 1

        except Exception as e:
            logger.error(f"Failed to download {ticker}: {e}")
            download_info["failed"] += 1
    
    logger.info(f"Pipeline finished. Info: {download_info}")
    return metadata

# Testing
if __name__ == "__main__":
    download_data(start_date="2019-01-01", end_date="2024-12-31", risk_free_ticker="^IRX", input_filename="tickers.txt", target_currency="GBP")