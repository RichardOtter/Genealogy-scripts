-- Enter B for birth, D for death, or M for marriage at the :event_type prompt.
-- Enter a place name or part of one at the :place prompt; LIKE wildcards are supported.
-- Marriage events are listed once for each spouse.

WITH
Parameters AS (
  SELECT UPPER(TRIM(:event_type)) AS EventType
),
PrimaryNames AS (
  SELECT OwnerID AS PersonID, Given, Surname
  FROM NameTable
  WHERE IsPrimary = 1
),
Events AS (
  SELECT
    e.EventID,
    e.OwnerID AS PersonID,
    e.Date,
    e.SortDate,
    ft.Name AS EventType,
    p.Name AS PlaceName
  FROM EventTable e
  JOIN FactTypeTable ft ON ft.FactTypeID = e.EventType
  JOIN PlaceTable p ON p.PlaceID = e.PlaceID
  CROSS JOIN Parameters prm
  WHERE e.OwnerType = 0
    AND (
      (prm.EventType = 'B' AND UPPER(TRIM(ft.GedcomTag)) = 'BIRT')
      OR (prm.EventType = 'D' AND UPPER(TRIM(ft.GedcomTag)) = 'DEAT')
    )
    AND LOWER(TRIM(p.Name)) LIKE '%' || LOWER(TRIM(:place)) || '%'

  UNION ALL

  SELECT
    e.EventID,
    f.FatherID AS PersonID,
    e.Date,
    e.SortDate,
    ft.Name AS EventType,
    p.Name AS PlaceName
  FROM EventTable e
  JOIN FactTypeTable ft ON ft.FactTypeID = e.EventType
  JOIN PlaceTable p ON p.PlaceID = e.PlaceID
  JOIN FamilyTable f ON f.FamilyID = e.OwnerID
  CROSS JOIN Parameters prm
  WHERE e.OwnerType = 1
    AND prm.EventType = 'M'
    AND UPPER(TRIM(ft.GedcomTag)) = 'MARR'
    AND f.FatherID IS NOT NULL
    AND LOWER(TRIM(p.Name)) LIKE '%' || LOWER(TRIM(:place)) || '%'

  UNION ALL

  SELECT
    e.EventID,
    f.MotherID AS PersonID,
    e.Date,
    e.SortDate,
    ft.Name AS EventType,
    p.Name AS PlaceName
  FROM EventTable e
  JOIN FactTypeTable ft ON ft.FactTypeID = e.EventType
  JOIN PlaceTable p ON p.PlaceID = e.PlaceID
  JOIN FamilyTable f ON f.FamilyID = e.OwnerID
  CROSS JOIN Parameters prm
  WHERE e.OwnerType = 1
    AND prm.EventType = 'M'
    AND UPPER(TRIM(ft.GedcomTag)) = 'MARR'
    AND f.MotherID IS NOT NULL
    AND LOWER(TRIM(p.Name)) LIKE '%' || LOWER(TRIM(:place)) || '%'
)
SELECT
  e.PersonID,
  COALESCE(n.Surname, '') ||
    CASE WHEN n.Surname IS NOT NULL AND n.Given IS NOT NULL THEN ', ' ELSE '' END ||
    COALESCE(n.Given, '') AS PersonName,
  CASE
    WHEN substr(e.Date, 1, 1) = 'D'
      AND substr(e.Date, 4, 4) <> '0000'
      AND substr(e.Date, 4, 4) GLOB '[0-9][0-9][0-9][0-9]'
      AND substr(e.Date, 8, 2) BETWEEN '00' AND '12'
      AND substr(e.Date, 10, 2) BETWEEN '00' AND '31'
      THEN
        CASE substr(e.Date, 2, 1)
          WHEN 'A' THEN 'after '
          WHEN 'B' THEN 'before '
          WHEN 'I' THEN 'since '
          WHEN 'U' THEN 'until '
          WHEN 'Y' THEN 'by '
          ELSE ''
        END ||
        CASE
          WHEN substr(e.Date, 10, 2) <> '00'
            THEN CAST(substr(e.Date, 10, 2) AS INTEGER) || ' '
          ELSE ''
        END ||
        CASE substr(e.Date, 8, 2)
          WHEN '01' THEN 'Jan '
          WHEN '02' THEN 'Feb '
          WHEN '03' THEN 'Mar '
          WHEN '04' THEN 'Apr '
          WHEN '05' THEN 'May '
          WHEN '06' THEN 'Jun '
          WHEN '07' THEN 'Jul '
          WHEN '08' THEN 'Aug '
          WHEN '09' THEN 'Sep '
          WHEN '10' THEN 'Oct '
          WHEN '11' THEN 'Nov '
          WHEN '12' THEN 'Dec '
          ELSE ''
        END ||
        substr(e.Date, 4, 4)
    ELSE e.Date
  END AS EventDate,
  e.EventType,
  e.PlaceName
FROM Events e
LEFT JOIN PrimaryNames n ON n.PersonID = e.PersonID
ORDER BY
  e.SortDate ASC,
  e.PlaceName COLLATE NOCASE ASC,
  PersonName ASC;
