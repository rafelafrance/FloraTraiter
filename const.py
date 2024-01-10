import os
from pathlib import Path

# #########################################################################
# Useful locations

CURR_DIR = Path(os.getcwd())
IS_SUBDIR = CURR_DIR.name in ("notebooks", "experiments")
ROOT_DIR = Path("../.." if IS_SUBDIR else ".")

DATA_DIR = ROOT_DIR / "data"

MODEL_PATH = DATA_DIR / "traiter_plants_model"

# #########################################################################
# Used for validating taxon names

MIN_TAXON_LEN = 3  # The entire taxon must be this long
MIN_TAXON_WORD_LEN = 2  # Each word in the taxon must be this long


# #########################################################################
EFLORAS_SITE = "http://www.efloras.org"

EFLORAS_DIR = DATA_DIR / "eFloras"
EFLORAS_FAMILIES = DATA_DIR / "efloras_families" / "eFloras_family_list.csv"
