# src/config.py
import os
from pathlib import Path
from dotenv import load_dotenv

# 1. Root directory of Project
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# 2. Loading variables from .env
load_dotenv(PROJECT_ROOT / ".env")

# 3. Function to get paths
def get_path(env_var: str, default_value: str) -> Path:
    """Resolves a path from an environment variable.
    
    If the path is relative, it appends it to PROJECT_ROOT.
    If the path is absolute, it returns it directly.

    Args:
        env_var (str): The name of the environment variable (e.g., 'RAW_PATH').
        default_value (str): The fallback relative path (e.g., 'data/raw').

    Returns:
        Path: The resolved absolute PosixPath/WindowsPath."""
    
    path_value = os.getenv(env_var, default_value)
    path_obj = Path(path_value)

    if path_obj.is_absolute():
        return path_obj
    
    return PROJECT_ROOT / path_value

# 4. Paths (from .env variables)
DATA_DIR = get_path("DATA_PATH", "data")
DATA_RAW_DIR = get_path("RAW_PATH", "data/raw")
DATA_PROCESSED_DIR = get_path("PROCESSED_PATH", "data/processed")
NOTEBOOKS_DIR = get_path("NOTEBOOKS_PATH", "notebooks")
REPORTS_DIR = get_path("REPORTS_PATH", "reports")
FIGURES_DIR = get_path("FIGURES_PATH", "reports/figures")
MISC_DIR = get_path("MISC", "misc")

# 5. Debugging
if __name__ == "__main__":
    # Quick verification of paths
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Raw Data Dir: {DATA_RAW_DIR}")
    print(f"Exists? {DATA_RAW_DIR.exists()}")