WITH Women AS (
    SELECT DISTINCT MotherID AS PersonID,
           FamilyID
    FROM FamilyTable
    WHERE MotherID IS NOT NULL AND MotherID > 0
),

MarriageEvents AS (
    SELECT et.OwnerID AS FamilyID
    FROM EventTable et
    JOIN FactTypeTable ftt ON et.EventType = ftt.FactTypeID
    WHERE et.OwnerType = 1
      AND ftt.Name IN ('Marriage', 'Partnership', 'Marriage License', 'Marriage Contract', 'Marriage Bann')
)

SELECT w.PersonID
FROM Women w
LEFT JOIN MarriageEvents me ON me.FamilyID = w.FamilyID
WHERE me.FamilyID IS NULL
ORDER BY w.PersonID;

