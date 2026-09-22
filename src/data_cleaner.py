import pandas as pd


def create_inspection_report(data: pd.DataFrame, ticker: str) -> dict:
    """
    Create an inspection report from a DataFrame

    Args:
        data: The DataFrame.
        ticker: The ticker name.

    Returns:
        dict: An inspection report for the specified ticker.

    Raises:
        TypeError: if `data` is not a DataFrame or `ticker` is not a string.
    """

    if not isinstance(data, pd.DataFrame):
        raise TypeError("Data must be a DataFrame.")

    if not isinstance(ticker, str):
        raise TypeError("Ticker must be a string.")

    inspection = {
        "ticker": ticker,
        "rows": data.shape[0],
        "column_names": data.columns.to_list(),
        "dtypes": data.dtypes.to_dict(),
        "start_date": data["Date"].min(),
        "end_date": data["Date"].max(),
        "missing_values": data.isna().sum().to_dict(),
        "duplicated_dates": data["Date"].duplicated().sum(),
        "date_sorted": data["Date"].is_monotonic_increasing
    }

    return inspection
