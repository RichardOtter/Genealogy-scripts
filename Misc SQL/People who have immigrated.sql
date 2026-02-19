  -- #-----------------------------------------------
  -- [Immigrated]
  -- SQL_QUERY =
  -- create a CTE so search criteria appear together & once
  WITH
  Constants AS ( SELECT
     'Immigration'   AS C_FactTypeName,
     'United States' AS C_Destination,
     'Germany'       AS C_Origin 
  ),
  --
  Selected_events AS
  (
  SELECT et.EventID
  FROM EventTable AS et 
  INNER JOIN FactTypeTable AS ftt ON et.EventType = ftt.FactTypeID
  INNER JOIN PlaceTable AS pt ON et.PlaceID = pt.PlaceID
  WHERE
      et.OwnerType = 0
  AND ftt.Name COLLATE NOCASE = (SELECT C_FactTypeName FROM Constants)
  AND et.Details LIKE ('%' || (SELECT C_Origin FROM Constants) || '%')
  AND pt.Name LIKE ('%' || (SELECT C_Destination FROM Constants) || '%')
  ),
  Selected_persons AS
  (
  -- get the people with the Fact attached
  SELECT et.OwnerID AS PersonID
  FROM EventTable AS et
  INNER JOIN Selected_events ON Selected_events.EventID = et.EventID
  UNION
  -- get the people with the Shared Fact attached
  SELECT wt.PersonID AS PersonID
  FROM WitnessTable AS wt
  INNER JOIN Selected_events ON Selected_events.EventID = wt.EventID
  )
  -- Generate the list of PersonIDs
  SELECT PersonID 
  FROM Selected_persons 
  ORDER BY PersonID ASC;

