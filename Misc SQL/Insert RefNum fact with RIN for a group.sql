

-- GroupID hardcoded to 1049
-- unused columns left null. RM usually inserts a 0.

-- The event table
--(EventID INTEGER PRIMARY KEY, EventType INTEGER, OwnerType INTEGER, OwnerID INTEGER, FamilyID INTEGER, PlaceID INTEGER, SiteID INTEGER, Date TEXT, SortDate BIGINT, IsPrimary INTEGER, IsPrivate INTEGER, Proof INTEGER, Status INTEGER, Sentence TEXT, Details TEXT, Note TEXT, UTCModDate FLOAT );


-- First check whether any RefNumber facts are already defined
SELECT et.OwnerID AS PersonID 
FROM EventTable AS et
WHERE et.EventType = 35;

-- Do any pre-existing RefNum rows have odd details?
SELECT et.OwnerID AS PersonID 
FROM EventTable AS et
WHERE et.Details <> et.OwnerID
AND et.EventType = 35;

-- optionally delete all RefNumber facts
DELETE
FROM EventTable
WHERE EventType = 35;

-- Insert the Reference Number events, but not if record already exists
INSERT INTO EventTable AS et (
    EventType,OwnerType,OwnerID, 
    Date, SortDate, Details,
    UTCModDate )
SELECT
      35, 0, pt.PersonID,
      '.', 9223372036854775807, pt.PersonID,
      julianday('now') - 2415018.5
FROM PersonTable AS pt
INNER JOIN GroupTable AS gt ON gt.GroupID = 1049
     AND pt.PersonID >= gt.StartID
     AND pt.PersonId <= gt.EndID
WHERE NOT EXISTS (
      SELECT OwnerID
      FROM EventTable AS et
      WHERE et.OwnerID = pt.PersonID
            AND et.EventType = 35
);
