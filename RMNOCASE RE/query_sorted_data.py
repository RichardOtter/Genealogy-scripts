"""
Read the RMNOCASE index order after RootsMagic rebuilds the database indexes.

The registered approximation only allows SQLite to recognize the collation;
the query must scan the existing index without sorting or changing the database.
"""

import sqlite3
from contextlib import closing
from pathlib import Path

from insert_test_data import DB_PATH, rmnocase


INDEX_QUERY = """
    SELECT PlaceID, Name FROM PlaceTable INDEXED BY idxPlaceName
    WHERE PlaceType = 0 ORDER BY Name
"""


def query_sorted_data():
    """Display and save test places in RootsMagic's index order."""
    db_path = Path(DB_PATH).resolve()
    with closing(sqlite3.connect(db_path.as_uri() + "?mode=ro", uri=True)) as conn:
        conn.create_collation("RMNOCASE", rmnocase)
        plan = conn.execute("EXPLAIN QUERY PLAN " + INDEX_QUERY).fetchall()
        details = [row[3].upper() for row in plan]
        if not any("IDXPLACENAME" in detail for detail in details) or any(
            "TEMP B-TREE" in detail for detail in details
        ):
            raise RuntimeError(f"Query cannot read the existing index order: {plan}")
        sorted_rows = conn.execute(INDEX_QUERY).fetchall()
        inserted_rows = conn.execute(
            "SELECT PlaceID, Name FROM PlaceTable WHERE PlaceType = 0 ORDER BY PlaceID"
        ).fetchall()

    print(f"Connected to database: {db_path}")
    print(f"Test places: {len(sorted_rows)}")
    print("\nROOTSMAGIC INDEX ORDER")
    for idx, (place_id, name) in enumerate(sorted_rows, 1):
        print(f"{idx:3d}. ID={place_id:3d}  Name={name!r}")

    print("\nPLACE ID ORDER")
    for idx, (place_id, name) in enumerate(inserted_rows, 1):
        print(f"{idx:3d}. ID={place_id:3d}  Name={name!r}")

    output_file = db_path.parent / "sorted_output.txt"
    with output_file.open("w", encoding="utf-8") as output:
        output.write("ROOTSMAGIC INDEX ORDER\n")
        for idx, (place_id, name) in enumerate(sorted_rows, 1):
            output.write(f"{idx:3d}. ID={place_id:3d}  Name={name!r}\n")
    print(f"\nOutput saved to: {output_file}")
    return True


if __name__ == "__main__":
    query_sorted_data()
