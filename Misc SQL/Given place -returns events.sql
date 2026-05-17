-- At prompt, enter place name with appropriate LIKE wildcards
-- Returns Birth, Death, and Marriage events that happened at the entered place

-- Replace :place with your pattern, e.g. '%Boston%'
WITH
PrimaryNames AS (
  SELECT OwnerID AS PersonID, Given, Surname
  FROM NameTable
  WHERE IsPrimary = 1
),

PersonEvents AS (
  SELECT
    e.EventID,
    e.OwnerID AS PersonID,
    ft.Name AS EventType,
    p.Name AS PlaceName,
    e.Date AS RawRMDate
  FROM EventTable e
  JOIN FactTypeTable ft ON ft.FactTypeID = e.EventType
  JOIN PlaceTable p ON p.PlaceID = e.PlaceID
  WHERE ft.Name IN ('Birth','Death')
    AND LOWER(TRIM(p.Name)) LIKE LOWER(:place)
    AND e.OwnerType = 0
),

MarriageEvents_Father AS (
  SELECT
    e.EventID,
    f.FatherID AS PersonID,
    ft.Name AS EventType,
    p.Name AS PlaceName,
    e.Date AS RawRMDate
  FROM EventTable e
  JOIN FactTypeTable ft ON ft.FactTypeID = e.EventType
  JOIN PlaceTable p ON p.PlaceID = e.PlaceID
  JOIN FamilyTable f ON f.FamilyID = e.OwnerID
  WHERE ft.Name = 'Marriage'
    AND LOWER(TRIM(p.Name)) LIKE LOWER(:place)
    AND e.OwnerType = 1
    AND f.FatherID IS NOT NULL
),

MarriageEvents_Mother AS (
  SELECT
    e.EventID,
    f.MotherID AS PersonID,
    ft.Name AS EventType,
    p.Name AS PlaceName,
    e.Date AS RawRMDate
  FROM EventTable e
  JOIN FactTypeTable ft ON ft.FactTypeID = e.EventType
  JOIN PlaceTable p ON p.PlaceID = e.PlaceID
  JOIN FamilyTable f ON f.FamilyID = e.OwnerID
  WHERE ft.Name = 'Marriage'
    AND LOWER(TRIM(p.Name)) LIKE LOWER(:place)
    AND e.OwnerType = 1
    AND f.MotherID IS NOT NULL
),

AllEvents AS (
  SELECT EventID, PersonID, EventType, PlaceName, RawRMDate FROM PersonEvents
  UNION ALL
  SELECT EventID, PersonID, EventType, PlaceName, RawRMDate FROM MarriageEvents_Father
  UNION ALL
  SELECT EventID, PersonID, EventType, PlaceName, RawRMDate FROM MarriageEvents_Mother
),

MatchedPlaces AS (
  SELECT DISTINCT PlaceName AS MatchedPlaceName
  FROM AllEvents
),

-- Header rows: one per matched place (show InputPlace and MatchedPlaceName once)
Header AS (
  SELECT
    :place AS InputPlace,
    mp.MatchedPlaceName,
    NULL AS PersonID,
    NULL AS PersonName,
    NULL AS EventType,
    NULL AS EventDate,
    NULL AS RawRMDate,
    mp.MatchedPlaceName AS sort_place,
    0 AS sort_key
  FROM MatchedPlaces mp
),

-- Event rows: actual results without repeating the place name (place used only for ordering)
EventRows AS (
  SELECT
    NULL AS InputPlace,
    NULL AS MatchedPlaceName,
    ae.PersonID,
    COALESCE(pn.Surname, '') ||
      CASE WHEN pn.Surname IS NOT NULL AND pn.Given IS NOT NULL THEN ', ' ELSE '' END ||
      COALESCE(pn.Given, '') AS PersonName,
    ae.EventType,
    -- Simple substring-based date extraction and formatting
    CASE
      WHEN ae.RawRMDate LIKE 'D%' AND LENGTH(ae.RawRMDate) >= 11
        THEN substr(ae.RawRMDate,4,4) || '-' || substr(ae.RawRMDate,8,2) || '-' || substr(ae.RawRMDate,10,2)
      ELSE ae.RawRMDate
    END AS EventDate,
    ae.RawRMDate,
    ae.PlaceName AS sort_place,  -- used only for ordering
    1 AS sort_key
  FROM AllEvents ae
  LEFT JOIN PrimaryNames pn ON pn.PersonID = ae.PersonID
  WHERE ae.PersonID IS NOT NULL
)

-- Combine header(s) and event rows; outer query hides the internal sort columns and orders by matched place
SELECT
  InputPlace,
  MatchedPlaceName,
  PersonID,
  PersonName,
  EventType,
  EventDate,
  RawRMDate
FROM (
  SELECT * FROM Header
  UNION ALL
  SELECT * FROM EventRows
) AS combined
ORDER BY combined.sort_place, combined.sort_key, PersonName;
