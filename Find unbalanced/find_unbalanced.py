import sqlite3
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = r"C:\Users\rotter\dev\Genealogy\repo Genealogy-scripts\Misc SQL\DB\TEST-Misc SQL.rmtree"
EXT_PATH = r"C:\Users\rotter\Genealogy\GeneDB\SW\SQLite extensions\unifuzz64.dll"

BRACKETS = [
    ('[', ']'),
    ('(', ')'),
    ('{', '}'),
    ('►', '◄'),
]

def count_char(s, ch):
    return s.count(ch) if s else 0

def is_unbalanced(value):
    if value is None:
        return False
    for open_b, close_b in BRACKETS:
        if count_char(value, open_b) != count_char(value, close_b):
            return True
    return False

def main():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database not found: {DB_PATH}")

    if not os.path.exists(EXT_PATH):
        raise FileNotFoundError(f"Extension not found: {EXT_PATH}")

    conn = sqlite3.connect(DB_PATH)
    conn.enable_load_extension(True)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    print("Loading RMNOCASE collation extension...")
    cur.execute(f"SELECT load_extension('{EXT_PATH}')")
    print("Extension loaded.\n")

    print("Running REINDEX RMNOCASE...")
    try:
        cur.execute("REINDEX RMNOCASE")
        print("REINDEX completed.\n")
    except sqlite3.Error as e:
        print(f"REINDEX failed: {e}\n")

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

        # Quote columns exactly as SQLite expects
        quoted_cols = [f'"{c}" AS "{c}"' for c in columns]
        col_list = ", ".join(quoted_cols)

        cur.execute(f'SELECT rowid AS "rowid", {col_list} FROM "{table}"')

        for row in cur.fetchall():
            rowid = row["rowid"]

            for col in columns:
                # Ensure column exists in row
                if col not in row.keys():
                    continue

                value = row[col]

                if is_unbalanced(value):
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

if __name__ == "__main__":
    main()

