-- WARNING- this does not back up data

BEGIN TRANSACTION;

CREATE TEMP VIEW uncertain_places AS
SELECT PlaceID
FROM PlaceTable
WHERE (
        Name LIKE '[~%' 
        OR Name LIKE '~%'
      )
  AND PlaceType = 1;

UPDATE EventTable
SET PlaceID = 0,
    SiteID = 0
WHERE PlaceID IN (SELECT PlaceID FROM uncertain_places);

DELETE FROM PlaceTable
WHERE PlaceID IN (SELECT PlaceID FROM uncertain_places);

DROP VIEW uncertain_places;

COMMIT;
