"""Project-wide constants."""
import os
from pathlib import Path

# Download site
SITE = "http://www.efloras.org"

BASE_DIR = Path.cwd().resolve().parts[-1]
BASE_DIR = Path.cwd() if BASE_DIR.find("floras") > -1 else Path.cwd().parent

CURR_DIR = Path(os.getcwd())
IS_SUBDIR = CURR_DIR.name in ("notebooks", "experiments")
ROOT_DIR = Path("../.." if IS_SUBDIR else ".")

DATA_DIR = ROOT_DIR / "data"
MOCK_DIR = ROOT_DIR / "tests" / "mock_data"

EFLORAS_DIR = DATA_DIR / "eFloras"
EFLORAS_FAMILIES = DATA_DIR / "efloras_families" / "eFloras_family_list.csv"
