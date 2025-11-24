# src/helpers_io.py
from pathlib import Path
from typing import Union
import pandas as pd

from .config import DATA_RAW_DIR, DATA_PROCESSED_DIR

PathLike = Union[str, Path]

# Building PATHs for 'raw' and 'processed' folders
def raw_path(filename: str) -> Path:
    "Returns the full path of a file in data/raw"
    return DATA_RAW_DIR / filename

def processed_path(filename: str) -> Path:
    "Returns the full path of a file in data/processed"
    return DATA_PROCESSED_DIR / filename

# Reading CSVs from 'raw' and 'processed' folders
def read_csv_raw(filename: str, **kwargs) -> pd.DataFrame:
    "Reads a CSV file from data/raw"
    return pd.read_csv(raw_path(filename), **kwargs)

def read_csv_processed(filename: str, **kwargs) -> pd.DataFrame:
    "Reads a CSV file from data/processed"
    return pd.read_csv(processed_path(filename), **kwargs)

# Saving CSV in 'processed' folder
def save_csv_processed(df: pd.DataFrame, filename: str, index: bool = False, **kwargs) -> None:
    "Saves a DataFrame in data/processed"
    filepath = processed_path(filename)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filepath, index=index, **kwargs)