from pathlib import Path

import pandas as pd
import yfinance as yf


def download_assets(
        asset_universe: list,
        start_date: str | pd.Timestamp,
        end_date: str | pd.Timestamp
    ) -> dict:

    """
    Download and validate historical price data for the asset universe

    Args:
        asset_universe: A list of asset tickers to download.
        start_date: The start date of the requested period.
        end_date: The exclusive end date of the requested period.

    Returns:
        dict: A dictionary containing the validated price DataFrame for each ticker.

    Raises:
        RuntimeError: If one or more asset datasets fail the required validation checks.
    """

    downloaded_data = {}
    errors = {}
    warnings = {}

    start = pd.Timestamp(start_date)
    end = pd.Timestamp(end_date)
    tolerance = pd.Timedelta(days=7)   # Allow for weekends and market holidays

    for ticker in asset_universe:
        data = yf.download(
            ticker,
            start=start_date,
            end=end_date,
            auto_adjust=True,
            progress=False,
            multi_level_index=False
        )

        errors[ticker] = []
        warnings[ticker] = []

        if data.empty:
            errors[ticker].append("⚠️ No data returned")
            continue

        data = data.reset_index()   # Move Date from index to column

        if not {"Date", "Close"}.issubset(data.columns):
            errors[ticker].append("⚠️ Missing required column: Date and/or Close")
            continue

        if data["Date"].isna().any():
            errors[ticker].append("⚠️ Missing values found in Date")

        if data["Date"].duplicated().any():
            warnings[ticker].append("⚠️ Duplicated dates found")

        if not data["Date"].is_monotonic_increasing:
            warnings[ticker].append("⚠️ Dates are not sorted chronologically")

        if data["Close"].isna().all():
            errors[ticker].append("⚠️ Close column contains only missing values")

        elif data["Close"].isna().any():
            warnings[ticker].append("⚠️ Missing values found in Close")

        min_date = data["Date"].min()
        max_date = data["Date"].max()

        if min_date > start + tolerance:
            errors[ticker].append(
                f"⚠️ Data starts too late: {min_date.date()}"
            )

        if max_date < end - tolerance:
            errors[ticker].append(
                f"⚠️ Data ends too early: {max_date.date()}"
            )

        if errors[ticker]:
            continue

        downloaded_data[ticker] = data

    failed_tickers = {
        ticker: ticker_errors
        for ticker, ticker_errors in errors.items()
        if ticker_errors
    }

    warning_tickers = {
        ticker: ticker_warnings
        for ticker, ticker_warnings in warnings.items()
        if ticker_warnings
    }

    if warning_tickers:
        print("⚠️ Warnings found:")
        for ticker, ticker_warnings in warning_tickers.items():
            print(f"{ticker}: {ticker_warnings}")

    if failed_tickers:
        raise RuntimeError(
            f"❌ Asset download validation failed: {failed_tickers}"
        )

    return downloaded_data

# Download risk-free rate from FRED
def download_risk_free(
        rf_rate_url: str,
        start_date: str | pd.Timestamp,
        end_date: str | pd.Timestamp,
        date_col_name: str,
        rf_col_name: str
    ) -> pd.DataFrame:

    """
    Download and validate the risk-free rate dataset from FRED

    Args:
        rf_rate_url: The URL used to download the FRED dataset.
        start_date: The start date of the requested period.
        end_date: The exclusive end date of the requested period.
        date_col_name: The original name of the date column.
        rf_col_name: The original name of the risk-free rate column.

    Returns:
        pd.DataFrame: The validated risk-free rate dataset with standardized column names.

    Raises:
        RuntimeError: If the risk-free dataset fails the required validation checks.
    """

    start = pd.Timestamp(start_date)
    end = pd.Timestamp(end_date)
    tolerance = pd.Timedelta(days=7)   # Allow for weekends and market holidays

    risk_free_errors = []
    risk_free_warnings = []

    risk_free = pd.read_csv(
        rf_rate_url,
        na_values="."
    )

    expected_columns = {date_col_name, rf_col_name}

    if not expected_columns.issubset(risk_free.columns):
        risk_free_errors.append(
            f"⚠️ Missing required columns: {sorted(expected_columns - set(risk_free.columns))}"
        )

    else:
        risk_free = risk_free.rename(
            columns={
                date_col_name: "Date",
                rf_col_name: "Risk_Free_Rate"
            }
        )

        risk_free["Date"] = pd.to_datetime(
            risk_free["Date"],
            errors="coerce"
        )

        if risk_free["Date"].isna().any():
            risk_free_errors.append("⚠️ Invalid or missing values found in Date")

        else:
            risk_free = risk_free[
                risk_free["Date"].between(
                    start,
                    end,
                    inclusive="left"
                )
            ].copy()

            if risk_free.empty:
                risk_free_errors.append("⚠️ No risk-free data returned for the selected period")

            else:
                if risk_free["Date"].duplicated().any():
                    risk_free_warnings.append("⚠️ Duplicated dates found")

                if not risk_free["Date"].is_monotonic_increasing:
                    risk_free_warnings.append("⚠️ Dates are not sorted chronologically")

                if risk_free["Risk_Free_Rate"].isna().all():
                    risk_free_errors.append(
                        "⚠️ Risk_Free_Rate column contains only missing values"
                    )

                elif risk_free["Risk_Free_Rate"].isna().any():
                    risk_free_warnings.append(
                        "⚠️ Missing observations found in Risk_Free_Rate"
                    )

                min_date = risk_free["Date"].min()
                max_date = risk_free["Date"].max()

                if min_date > start + tolerance:
                    risk_free_errors.append(
                        f"⚠️ Risk-free data starts too late: {min_date.date()}"
                    )

                if max_date < end - tolerance:
                    risk_free_errors.append(
                        f"⚠️ Risk-free data ends too early: {max_date.date()}"
                    )

    if risk_free_warnings:
        print("⚠️ Risk-free warnings:")
        for warning in risk_free_warnings:
            print(f"- {warning}")

    if risk_free_errors:
        raise RuntimeError(
            f"⚠️ Risk-free download validation failed: {risk_free_errors}"
        )

    return risk_free

# Save validated raw data
def save_raw_data(
        downloaded_data: dict,
        risk_free: pd.DataFrame,
        raw_dir: Path,
        rf_name: str
    ) -> None:

    """
    Save validated asset and risk-free datasets to the raw data directory

    Args:
        downloaded_data: A dictionary containing the validated asset price datasets.
        risk_free: The validated risk-free rate DataFrame.
        raw_dir: The directory where the raw datasets will be saved.
        rf_name: The name used for the risk-free rate output file.

    Returns:
        None
    """

    files_saved = []

    for ticker, data in downloaded_data.items():
        filename = f"{ticker}_prices.csv"
        filepath = raw_dir / filename

        data.to_csv(filepath, index=False)
        files_saved.append(filename)

    risk_free_filename = f"{rf_name}_rate.csv"
    risk_free_filepath = raw_dir / risk_free_filename

    risk_free.to_csv(risk_free_filepath, index=False)
    files_saved.append(risk_free_filename)

    # Final summary
    print("✅ All datasets passed required validation and were saved successfully.")
    print(f"✅ {len(files_saved)} files saved in {raw_dir}")