import sys
from pathlib import Path
sys.path.append(str(Path.resolve(Path(__file__).resolve().parent / '../RMpy package')))

import RMpy.launched_from_explorer as RMl       # noqa #type: ignore

import sqlite3


def main():
    db_path = Path(r"C:\Users\rotter\Genealogy\GeneDB\Otter-Saito.rmtree")

    sql = """\
      SELECT *
        FROM (
            SELECT PersonID,  Surname || ', ' || Given
            FROM PersonTable AS pt
            INNER JOIN NameTable AS nt ON nt.OwnerID = pt.PersonID
            WHERE nt.IsPrimary = 1
            ORDER BY PersonID DESC
            LIMIT 30
        )
        ORDER BY PersonID ASC;
    """

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    print("The last 30 People entered into RM\n")

    for pid, name in cur.execute(sql):
        print(f"{pid:6}  {name}")

    conn.close()

    if RMl.launched_from_explorer():
        input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()