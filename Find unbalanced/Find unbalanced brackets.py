import sys
sys.stdout.reconfigure(encoding='utf-8')

import os
import sqlite3

# PRODUCTION
DB_PATH = r"C:\Users\rotter\Genealogy\GeneDB\Otter-Saito.rmtree"

BRACKETS = [
    ('[', ']'),
    ('(', ')'),
    ('{', '}'),
    ('►', '◄'),
]

EXCEPTIONS_LIST = [
    'eigene Person:',
    'Legal Notice',
    '_TYPOS-IN-ORIGINAL',
]

def main():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database not found: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Get all user tables
    cur.execute("""
        SELECT name 
        FROM sqlite_master 
        WHERE type='table' 
          AND name NOT LIKE 'sqlite_%'
    """)
    tables = [row["name"] for row in cur.fetchall()]

    print(f"Scanning {len(tables)} tables...\n")

    results = []

    for table in tables:
        # Get TEXT columns
        cur.execute(f'PRAGMA table_info("{table}")')
        pragma_rows = cur.fetchall()

        columns = []
        for row in pragma_rows:
            colname = row["name"]
            coltype = row["type"].upper()
            if "CHAR" in coltype or "TEXT" in coltype:
                columns.append(colname)

        if not columns:
            continue

        # Quote + apply NOCASE collation
        quoted_cols = [f'"{c}" COLLATE NOCASE AS "{c}"' for c in columns]
        col_list = ", ".join(quoted_cols)

        cur.execute(f'SELECT rowid AS "rowid", {col_list} FROM "{table}"')

        for row in cur.fetchall():
            rowid = row["rowid"]

            for col in columns:
                if col not in row.keys():
                    continue

                value = row[col]

                if is_unbalanced(value):
                    if contains_any(value, EXCEPTIONS_LIST):
                        continue

                    counts = {
                        f"{open_b}_count": count_char(value, open_b)
                        for open_b, _ in BRACKETS
                    }
                    counts.update({
                        f"{close_b}_count": count_char(value, close_b)
                        for _, close_b in BRACKETS
                    })

                    results.append({
                        "table": table,
                        "column": col,
                        "rowid": rowid,
                        "value": value,
                        **counts
                    })

    if not results:
        print("No unbalanced brackets found.")
        return

    print("Unbalanced bracket issues found:\n")
    for r in results:
        print(f"Table: {r['table']}, Column: {r['column']}, RowID: {r['rowid']}")
        print(f"Value: {r['value']}")
        print("Counts:", {k: v for k, v in r.items() if k.endswith("_count")})
        print("-" * 60)


def count_char(s, ch):
    return s.count(ch) if s else 0

def is_unbalanced(value):
    if value is None:
        return False
    for open_b, close_b in BRACKETS:
        if count_char(value, open_b) != count_char(value, close_b):
            return True
    return False


def contains_any(text: str, keywords: list[str]) -> bool:
    return any(k in text for k in EXCEPTIONS_LIST)

if __name__ == "__main__":
    main()

    