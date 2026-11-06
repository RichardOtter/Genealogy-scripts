import argparse
import sqlite3
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent / '../RMpy package'))

import RMpy.RMDate              # noqa #type: ignore

DEFAULT_DATABASE = r"C:\Users\rotter\Genealogy\GeneDB\Otter-Saito.rmtree"


def main():
    parser = argparse.ArgumentParser(
        description="List RootsMagic birth, death, or marriage events at a place."
    )
    parser.add_argument(
        "database",
        nargs="?",
        default=DEFAULT_DATABASE,
        help=f"path to the RootsMagic database (default: {DEFAULT_DATABASE})",
    )
    args = parser.parse_args()

    # Launchers may pass a config .ini file here; only a database path overrides the default.
    if Path(args.database).suffix.lower() == ".ini":
        args.database = DEFAULT_DATABASE
    database_path = Path(args.database)
    if not database_path.is_file():
        parser.error(f"database file not found: {database_path}")

    event_type = input("Event type: B=birth, D=death, M=marriage: ").strip().upper()
    if event_type not in {"B", "D", "M"}:
        parser.error("event type must be B (birth), D (death), or M (marriage)")
    place = input("Place name or part of one: ").strip()

    with sqlite3.connect(database_path) as connection:
        # Stand-in for RM's RMNOCASE collation so the DLL isn't needed
        connection.create_collation("RMNOCASE", lambda a, b: (a.casefold() > b.casefold()) - (a.casefold() < b.casefold()))
        rows = get_report_rows(connection, event_type, place)

    if not rows:
        print("No matching events found.")
        return

    headings = ("PersonID", "PersonName", "EventDate", "EventType", "PlaceName")
    widths = [
        max(len(heading), *(len(str(row[index])) for row in rows))
        for index, heading in enumerate(headings)
    ]
    print(" ".join(heading.ljust(widths[index]) for index, heading in enumerate(headings)))
    print(" ".join("-" * width for width in widths))
    for row in rows:
        print(" ".join(str(value).ljust(widths[index]) for index, value in enumerate(row[:5])))
        print(f"    child of {row[5]} and {row[6]}")
        print()


EVENTS_SQL = """
WITH
PrimaryNames AS (
    SELECT OwnerID AS PersonID, Given, Surname
    FROM NameTable
    WHERE IsPrimary = 1
),
PrimaryParents AS (
    SELECT p.PersonID, f.FatherID, f.MotherID
    FROM PersonTable AS p
    LEFT JOIN FamilyTable AS f ON f.FamilyID = p.ParentID
),
Events AS (
    SELECT
        e.EventID,
        e.OwnerID AS PersonID,
        e.Date,
        e.SortDate,
        ft.Name AS EventType,
        p.Name AS PlaceName
    FROM EventTable AS e
    JOIN FactTypeTable AS ft ON ft.FactTypeID = e.EventType
    JOIN PlaceTable AS p ON p.PlaceID = e.PlaceID
    WHERE e.OwnerType = 0
      AND (
          (? = 'B' AND UPPER(TRIM(ft.GedcomTag)) = 'BIRT')
          OR (? = 'D' AND UPPER(TRIM(ft.GedcomTag)) = 'DEAT')
      )
      AND LOWER(TRIM(p.Name)) LIKE '%' || LOWER(TRIM(?)) || '%'

    UNION ALL

    SELECT
        e.EventID,
        f.FatherID AS PersonID,
        e.Date,
        e.SortDate,
        ft.Name AS EventType,
        p.Name AS PlaceName
    FROM EventTable AS e
    JOIN FactTypeTable AS ft ON ft.FactTypeID = e.EventType
    JOIN PlaceTable AS p ON p.PlaceID = e.PlaceID
    JOIN FamilyTable AS f ON f.FamilyID = e.OwnerID
    WHERE e.OwnerType = 1
      AND ? = 'M'
      AND UPPER(TRIM(ft.GedcomTag)) = 'MARR'
      AND f.FatherID IS NOT NULL
      AND LOWER(TRIM(p.Name)) LIKE '%' || LOWER(TRIM(?)) || '%'

    UNION ALL

    SELECT
        e.EventID,
        f.MotherID AS PersonID,
        e.Date,
        e.SortDate,
        ft.Name AS EventType,
        p.Name AS PlaceName
    FROM EventTable AS e
    JOIN FactTypeTable AS ft ON ft.FactTypeID = e.EventType
    JOIN PlaceTable AS p ON p.PlaceID = e.PlaceID
    JOIN FamilyTable AS f ON f.FamilyID = e.OwnerID
    WHERE e.OwnerType = 1
      AND ? = 'M'
      AND UPPER(TRIM(ft.GedcomTag)) = 'MARR'
      AND f.MotherID IS NOT NULL
      AND LOWER(TRIM(p.Name)) LIKE '%' || LOWER(TRIM(?)) || '%'
)
SELECT
    e.PersonID,
    COALESCE(n.Surname, '') ||
        CASE WHEN n.Surname IS NOT NULL AND n.Given IS NOT NULL
             THEN ', ' ELSE '' END ||
        COALESCE(n.Given, '') AS PersonName,
    e.Date AS RawDate,
    e.EventType,
    e.PlaceName,
    CASE WHEN father.PersonID IS NULL
         THEN 'Unknown'
         ELSE COALESCE(father.Surname, '') ||
              CASE WHEN father.Surname IS NOT NULL AND father.Given IS NOT NULL
                   THEN ', ' ELSE '' END ||
              COALESCE(father.Given, '')
    END AS FatherName,
    CASE WHEN mother.PersonID IS NULL
         THEN 'Unknown'
         ELSE COALESCE(mother.Surname, '') ||
              CASE WHEN mother.Surname IS NOT NULL AND mother.Given IS NOT NULL
                   THEN ', ' ELSE '' END ||
              COALESCE(mother.Given, '')
    END AS MotherName,
    e.SortDate
FROM Events AS e
LEFT JOIN PrimaryNames AS n ON n.PersonID = e.PersonID
LEFT JOIN PrimaryParents AS pp ON pp.PersonID = e.PersonID
LEFT JOIN PrimaryNames AS father ON father.PersonID = pp.FatherID
LEFT JOIN PrimaryNames AS mother ON mother.PersonID = pp.MotherID
ORDER BY e.SortDate ASC, e.PlaceName COLLATE NOCASE ASC, PersonName ASC;
"""


def format_rm_date(raw_date):
    if not raw_date:
        return ""
    try:
        return RMpy.RMDate.RMDate_str_TO_en_str(raw_date, RMpy.RMDate.Format.SHORT)
    except Exception:
        # date types not supported by RMpy.RMDate (Quaker, Quarter, slash dates)
        return raw_date


def get_report_rows(connection, event_type, place):
    event_type = event_type.strip().upper()
    if event_type not in {"B", "D", "M"}:
        raise ValueError("Event type must be B (birth), D (death), or M (marriage).")

    parameters = (event_type, event_type, place, event_type, place, event_type, place)
    rows = connection.execute(EVENTS_SQL, parameters).fetchall()
    return [
        (
            person_id,
            name,
            format_rm_date(raw_date),
            event_name,
            place_name,
            father_name,
            mother_name,
        )
        for (
            person_id,
            name,
            raw_date,
            event_name,
            place_name,
            father_name,
            mother_name,
            _sort_date,
        ) in rows
    ]


if __name__ == "__main__":
    main()
