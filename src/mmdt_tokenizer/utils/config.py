import os
from pathlib import Path

# === File Paths ===
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR =  PROJECT_ROOT /  "data"
OUTPUT_DIR = PROJECT_ROOT /  "result"

DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


DICT_FILE_PATH = DATA_DIR / "myg2p_mypos.dict" # FIXMED - NOT USE


