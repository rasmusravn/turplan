import json
from pathlib import Path

DATA_FILE = Path("ture.json")


def load_data():
    """Hent ture fra JSON-fil."""
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
        return [Tur(**tur) for tur in data]


def save_data(ture):
    """Gem ture til JSON-fil."""
    with open(DATA_FILE, "w") as f:
        json.dump([tur.__dict__ for tur in ture], f, indent=4)
