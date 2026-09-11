"""Populate AuxPlaceTable by running the three local SQL scripts in order."""

import configparser
import sqlite3
from pathlib import Path


SCRIPT_DIRECTORY = Path(__file__).parent
CONFIG_PATH = SCRIPT_DIRECTORY / "RM-Python-config.ini"
SQL_SCRIPTS = (
    "Initialize AuxPlace tables.sql",
    "Populate Uncertain from place names.sql",
    "Populate NonFSPlace from place names.sql",
)


def main():
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH, encoding="utf-8")
    database_path = Path(config["FILE_PATHS"]["DB_PATH"])
    if not database_path.is_absolute():
        database_path = CONFIG_PATH.parent / database_path

    connection = sqlite3.connect(database_path)
    try:
        connection.execute("PRAGMA foreign_keys = ON")
        for script_name in SQL_SCRIPTS:
            script_path = SCRIPT_DIRECTORY / script_name
            connection.executescript(script_path.read_text(encoding="utf-8"))
            print(f"Completed: {script_name}")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
