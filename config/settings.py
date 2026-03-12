# config/settings.py

import os
from dotenv import load_dotenv
from pathlib import Path

# Get project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env from root
load_dotenv(BASE_DIR / ".env")

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", 10))

print("DB_HOST:", DB_HOST)  # temporary debug