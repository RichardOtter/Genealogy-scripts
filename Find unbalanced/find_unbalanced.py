import sys
sys.stdout.reconfigure(encoding='utf-8')

import sqlite3

# PRODUCTION
DB_PATH = r"C:\Users\rotter\Genealogy\GeneDB\Otter-Saito.rmtree"

BRACKETS = [
    ('[', ']'),
    ('(', ')'),
    ('{', '}'),
    ('►', '◄'),
]

def has_unbalanced_brackets(value: str) -> bool:
    if value is None:
        return False

    counters = {pair: 0 for pair in BRACKETS}

    for ch in value:
        for left, right in BRACKETS:
            if ch == left:
                counters[(left, right)] += 1
            elif ch == right:
                counters[(left, right)] -= 1
                if counters[(left, right)] < 0:
                    return True

    return any(count != 0 for count in counters.values())

def bracket_report(value: str):
    report = {}
    for left, right in BRACKETS:
        left_count = value.count(left)
        right_count = value.count(right)
        report[(left, right)] = (left_count, right_count)
    return report

def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute(
        "SELECT name FROM sqlite_master "
        "WHERE type='table' ORDER BY name COLLATE NOCASE;"
    )
    tables = [row["name"] for row in cur.fetchall()]

    for table in tables:
        cur.execute(f"PRAGMA table_info('{table}')")
        cols_info = cur.fetchall()
        text_columns = [c["name"] for c in cols_info if c["type"].upper() == "TEXT"]

        if not text_columns:
            continue

        print(f"\nScanning table: {table}")

        sql = f'SELECT *, rowid FROM "{table}" ORDER BY rowid;'

        for row in cur.execute(sql):
            row_keys = row.keys()

            pk_cols = [c["name"] for c in cols_info if c["pk"] > 0]

            if pk_cols and pk_cols[0] in row_keys:
                id_col = pk_cols[0]
            elif "rowid" in row_keys:
                id_col = "rowid"
            else:
                id_col = None

            identifier = row[id_col] if id_col else None

            for col in text_columns:
                val = row[col]
                if isinstance(val, str) and has_unbalanced_brackets(val):
                    print(
                        f"  Unbalanced brackets in {table}.{col} "
                        f"({id_col}={identifier}): {val}"
                    )

                    # Bracket report
                    counts = bracket_report(val)
                    for (left, right), (lc, rc) in counts.items():
                        print(f"    {left}{right} count: {lc} left, {rc} right")

    conn.close()

if __name__ == "__main__":
    main()

    