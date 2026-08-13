import sqlite3

DB = r"C:\Users\rotter\Genealogy\GeneDB\Otter-Saito.rmtree"
EXT = r"C:\Users\rotter\Genealogy\GeneDB\SW\SQLite extensions\unifuzz64.dll"

def main():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    # --- Load SQLite extension ---
    conn.enable_load_extension(True)
    cur.execute(f"SELECT load_extension('{EXT}')")

    # --- Get Birth NameTypeID ---
    cur.execute("""
        SELECT NameTypeID
        FROM LU_NameType
        WHERE NameType = 'Birth'
    """)
    row = cur.fetchone()
    if row is None:
        raise ValueError("Birth NameTypeID not found in LU_NameType")
    birth_type_id = row[0]

    # --- Ensure reorganized AuxNameTypeException table exists ---
    cur.execute("""
        CREATE TABLE IF NOT EXISTS AuxNameTypeException (
            AuxNameID INTEGER PRIMARY KEY AUTOINCREMENT,
            PersonID INTEGER UNIQUE
        )
    """)

    # --- Query: primary name type = 0, excluding exceptions ---
    cur.execute("""
        WITH PrimaryNames AS (
            SELECT n.OwnerID AS PersonID,
                   n.NameType AS PrimaryNameTypeID,
                   n.Surname,
                   n.Given,
                   n.NameID
            FROM NameTable n
            WHERE n.IsPrimary = 1
        )
        SELECT pn.PersonID,
               pn.NameID,
               pn.Given,
               pn.Surname,
               pn.PrimaryNameTypeID
        FROM PrimaryNames pn
        WHERE pn.PrimaryNameTypeID = 0
          AND pn.PersonID NOT IN (
                SELECT PersonID FROM AuxNameTypeException
          )
        ORDER BY pn.PersonID
    """)

    rows = cur.fetchall()

    for person_id, name_id, given, surname, nametype in rows:
        full_name = f"{given} {surname}".strip()
        print(f"\nPersonID {person_id}: {full_name}")
        print(f"Primary NameType = {nametype}")
        print("Commands: B = convert to Birth, N = add exception, Q = quit")

        choice = input("Enter command: ").strip().upper()

        if choice == "Q":
            print("\nQuitting.")
            break

        elif choice == "B":
            cur.execute("""
                UPDATE NameTable
                SET NameType = ?
                WHERE NameID = ?
            """, (birth_type_id, name_id))
            conn.commit()
            print(f"Updated PersonID {person_id} primary name to Birth type.")

        elif choice == "N":
            cur.execute("""
                INSERT OR IGNORE INTO AuxNameTypeException (PersonID)
                VALUES (?)
            """, (person_id,))
            conn.commit()
            print(f"Added PersonID {person_id} to AuxNameTypeException.")

        else:
            print("Invalid input; skipping.")

    conn.close()
    print("\nDone.")

if __name__ == "__main__":
    main()
