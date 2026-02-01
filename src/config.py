# src/config.py
from pathlib import Path
import os
from dotenv import load_dotenv

# 1. Root directory of Project
ROOT_DIR = Path(__file__).resolve().parents[1]

# 2. Loading variables from .env
load_dotenv(ROOT_DIR / ".env")

# 3. Paths (from .env variables)
DATA_RAW_DIR = ROOT_DIR / os.getenv("RAW_PATH", "data/raw")
DATA_PROCESSED_DIR = ROOT_DIR / os.getenv("PROCESSED_PATH", "data/processed")
NOTEBOOKS_DIR = ROOT_DIR / os.getenv("NOTEBOOKS_PATH", "notebooks")
REPORTS_DIR = ROOT_DIR / os.getenv("REPORTS_PATH", "reports")
FIGURES_DIR = ROOT_DIR / os.getenv("FIGURES_PATH", "reports/figures")
MISC_DIR = ROOT_DIR / os.getenv("MISC", "misc")