# services/keyword_loader.py
import json
from pathlib import Path

KEYWORD_FILE = Path("memory/keywords.json")

def load_keywords():
    if not KEYWORD_FILE.exists():
        return []

    with KEYWORD_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)