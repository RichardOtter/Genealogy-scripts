

-- GroupID hardcoded to 1049
-- unused columns left null. RM usually inserts a 0.


-- First check whether some RefNumber facts are already defined
SELECT et.OwnerID AS PersonID 
FROM EventTable AS et
WHERE et.Details <> et.OwnerID
AND et.EventType = 35;

-- optionally delete all RefNumber facts
DELETE
FROM EventTable
WHERE EventType = 35;

-- Insert the Reference Number events
INSERT INTO EventTable (EventType,OwnerType,OwnerID, SortDate, Details, UTCModDate )
SELECT 
35,
0,
pt.PersonID,
9223372036854775807,
pt.PersonID,
julianday('now') - 2415018.5
FROM PersonTable AS pt
INNER JOIN GroupTable AS gt ON gt.GroupID = 1049
     AND pt.PersonID >= gt.StartID
     AND pt.PersonId <= gt.EndID;