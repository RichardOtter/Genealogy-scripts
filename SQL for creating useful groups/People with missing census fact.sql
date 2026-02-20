--[missing: FACT-Census: 1940]
--SQL_QUERY =
  -- Search for people with missing Census with constraints:
  -- people who might be in census but have no Census or Census_research FACT or SHARED FACT
  -- Requires Birth place in C_PlaceBirth
  -- Requires Birth birth date in specified range (between C_YearBirth and YearCensus)
  -- Death date after YearCensus or no DeathFact
  -- Person does not have a Census fact or shared census fact (Description starts with C_YearCensus)
  -- Does not find people not born in C_PlaceBirth but residing in USA in YearCensus
  -- Does not support Census Family type event.
  -- TO USE: Edit values in the constants section below.
  --
  WITH
  constants AS (SELECT
     1950            AS C_YearCensus,
     1850            AS C_YearBirth,
     'United States' AS C_PlaceBirth
  ),
  existing_events AS
  -- Census & Census_research events whose date YYYY=C_YearCensus
  (
  SELECT EventID
  FROM EventTable AS et
  INNER JOIN FactTypeTable AS ftt ON et.EventType = ftt.FactTypeID
  WHERE
    et.OwnerType = 0
    AND CAST(SUBSTR(et.Date, 4,4) as Integer) = (SELECT C_YearCensus FROM constants)
    AND (ftt.Name COLLATE NOCASE = 'Census' OR ftt.Name COLLATE NOCASE = 'Census_research')
  )
  --
  SELECT personID
  -- get all people who might have had a census event
  FROM PersonTable AS pt
    INNER JOIN PlaceTable AS plt ON et_birth.PlaceID = plt.PlaceID
    INNER JOIN EventTable AS et_birth ON et_birth.OwnerID = pt.PersonID
                                      AND et_birth.EventType = 1
    LEFT JOIN EventTable AS et_death  ON et_death.OwnerID = pt.PersonID
                                      AND et_death.EventType = 2
  WHERE
    plt.Name LIKE '%' || (SELECT C_PlaceBirth FROM Constants) || '%'
    AND  CAST(SUBSTR(et_birth.DATE, 4,4) as Integer) < CAST((SELECT C_YearCensus FROM Constants) as Integer)
    AND  CAST(SUBSTR(et_birth.DATE, 4,4) as Integer) > CAST((SELECT C_YearBirth FROM Constants) as Integer)
    AND ( CAST(SUBSTR(et_death.DATE, 4,4) as Integer) > CAST((SELECT C_YearCensus FROM Constants) as Integer)
          OR et_death.OwnerID IS NULL)
  --
  EXCEPT
  -- people who have a census fact of C_YearCensus
  SELECT et.OwnerID
  FROM EventTable AS et
  INNER JOIN existing_events ON existing_events.EventID = et.EventID
  --
  EXCEPT
  -- people who are witness to a census fact of C_YearCensus
  SELECT wt.PersonID
  FROM WitnessTable AS wt
  INNER JOIN existing_events ON existing_events.EventID = wt.EventID
  --
  ORDER BY 1 ASC;
  --
