-- database: C:\Users\rotter\dev\Genealogy\repo Genealogy-scripts\Misc SQL\DB\TEST-Misc SQL.rmtree

-- This SQL uses dates from the EventTable records so it can handle date
-- modifiers missing in the denormalized dates in the NameTable

-- Not yet tested for multiple events with same name
-- Should handle Family type events, but not fully tested

--#-----------------------------------------------
--[GRP: Died before age 10]
--SQL_QUERY =
  WITH Constants AS (
      SELECT
          'Birth' AS EventA,
          'Death' AS EventB,
          10      AS YearSpan
  ),
  -- Expand EventA to PersonID
  EventA AS (
      -- Person-level
      SELECT
          e.OwnerID AS PersonID,
          e.Date AS DateTextA,
          CAST(SUBSTR(e.Date, 4, 4) AS INTEGER) AS YearA
      FROM EventTable e
      JOIN FactTypeTable f
          ON f.FactTypeID = e.EventType
         AND f.Name COLLATE NOCASE = (SELECT EventA FROM Constants)
      WHERE e.OwnerType = 0
        AND e.Date LIKE 'D.%'
  --
      UNION ALL
  --
      -- Family-level → Father
      SELECT
          ft.FatherID AS PersonID,
          e.Date AS DateTextA,
          CAST(SUBSTR(e.Date, 4, 4) AS INTEGER) AS YearA
      FROM EventTable e
      JOIN FactTypeTable f
          ON f.FactTypeID = e.EventType
         AND f.Name COLLATE NOCASE = (SELECT EventA FROM Constants)
      JOIN FamilyTable ft
          ON ft.FamilyID = e.OwnerID
      WHERE e.OwnerType = 1
        AND ft.FatherID > 0
        AND e.Date LIKE 'D.%'
  --
      UNION ALL
  --
      -- Family-level → Mother
      SELECT
          ft.MotherID AS PersonID,
          e.Date AS DateTextA,
          CAST(SUBSTR(e.Date, 4, 4) AS INTEGER) AS YearA
      FROM EventTable e
      JOIN FactTypeTable f
          ON f.FactTypeID = e.EventType
         AND f.Name COLLATE NOCASE = (SELECT EventA FROM Constants)
      JOIN FamilyTable ft
          ON ft.FamilyID = e.OwnerID
      WHERE e.OwnerType = 1
        AND ft.MotherID > 0
        AND e.Date LIKE 'D.%'
  ),
  -- Expand EventB to PersonID
  EventB AS (
      -- Person-level
      SELECT
          e.OwnerID AS PersonID,
          e.Date AS DateTextB,
          CAST(SUBSTR(e.Date, 4, 4) AS INTEGER) AS YearB
      FROM EventTable e
      JOIN FactTypeTable f
          ON f.FactTypeID = e.EventType
         AND f.Name COLLATE NOCASE = (SELECT EventB FROM Constants)
      WHERE e.OwnerType = 0
        AND e.Date LIKE 'D.%'
  --
      UNION ALL
      -- Family-level → Father
      SELECT
          ft.FatherID AS PersonID,
          e.Date AS DateTextB,
          CAST(SUBSTR(e.Date, 4, 4) AS INTEGER) AS YearB
      FROM EventTable e
      JOIN FactTypeTable f
          ON f.FactTypeID = e.EventType
         AND f.Name COLLATE NOCASE = (SELECT EventB FROM Constants)
      JOIN FamilyTable ft
          ON ft.FamilyID = e.OwnerID
      WHERE e.OwnerType = 1
        AND ft.FatherID > 0
        AND e.Date LIKE 'D.%'
  --
      UNION ALL
      -- Family-level → Mother
      SELECT
          ft.MotherID AS PersonID,
          e.Date AS DateTextB,
          CAST(SUBSTR(e.Date, 4, 4) AS INTEGER) AS YearB
      FROM EventTable e
      JOIN FactTypeTable f
          ON f.FactTypeID = e.EventType
         AND f.Name COLLATE NOCASE = (SELECT EventB FROM Constants)
      JOIN FamilyTable ft
          ON ft.FamilyID = e.OwnerID
      WHERE e.OwnerType = 1
        AND ft.MotherID > 0
        AND e.Date LIKE 'D.%'
  )
  SELECT p.PersonID
  FROM EventA a
  JOIN EventB b ON b.PersonID = a.PersonID
  JOIN PersonTable p ON p.PersonID = a.PersonID
  LEFT JOIN NameTable n
      ON n.OwnerID = p.PersonID
     AND n.IsPrimary = 1
  WHERE (b.YearB - a.YearA) < (SELECT YearSpan FROM Constants);
  