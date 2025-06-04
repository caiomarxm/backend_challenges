import sqlite3
from pathlib import Path

from src.config.settings import settings


def create_db_file_if_not_exists():
    db_file = Path(settings.SQLITE_PATH)

    if not db_file.exists():
        print("Creating database")
        db_file.parent.mkdir(parents=True, exist_ok=True)
        sqlite3.connect(db_file)

    else:
        print("SQLite file already exists")


if __name__ == "__main__":
    create_db_file_if_not_exists()
