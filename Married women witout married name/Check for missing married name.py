import sqlite3
from datetime import datetime, timedelta

DB_PATH = "your_rootsmagic11_file.rmgc"  # Replace with your actual file path

# FactType codes (adjust if needed)
FACTTYPE_MARRIAGE = 3  # Marriage event


def main():
    conn = sqlite3.connect(DB_PATH)
    women_ids = get_women_without_name_near_marriage(conn)

    print("Women without name within 1 year of marriage:")
    for pid in women_ids:
        print(f"PersonID: {pid}")

    conn.close()

    
def parse_date(date_str):
    """Convert RM date string to datetime object. Adjust if using Julian."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except:
        return None

def get_women_without_name_near_marriage(conn):
    cursor = conn.cursor()

    # Get all female persons
    cursor.execute("""
        SELECT PersonID
        FROM PersonTable
        WHERE Sex = 1
    """)
    women = [row[0] for row in cursor.fetchall()]
    results = []

    for person_id in women:
        # Get marriage facts
        cursor.execute("""
            SELECT FactDate
            FROM FactTable
            WHERE OwnerID = ? AND FactType = ?
        """, (person_id, FACTTYPE_MARRIAGE))
        marriage_dates = [parse_date(row[0]) for row in cursor.fetchall() if parse_date(row[0])]

        if not marriage_dates:
            continue

        # Get name entries
        cursor.execute("""
            SELECT NameDate
            FROM NameTable
            WHERE OwnerID = ?
        """, (person_id,))
        name_dates = [parse_date(row[0]) for row in cursor.fetchall() if parse_date(row[0])]

        # Check if any name is within ±1 year of any marriage
        has_name_near_marriage = False
        for m_date in marriage_dates:
            for n_date in name_dates:
                if abs((m_date - n_date).days) <= 365:
                    has_name_near_marriage = True
                    break
            if has_name_near_marriage:
                break

        if not has_name_near_marriage:
            results.append(person_id)

    return results


if __name__ == "__main__":
    main()
    