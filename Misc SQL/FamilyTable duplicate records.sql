-- List FamilyTable records which have identicaL
-- FatherID and MotherID
-- Need a script to merge them and attachments.

SELECT *
FROM FamilyTable
WHERE (FatherID, MotherID) IN (
    SELECT FatherID, MotherID
    FROM FamilyTable
    GROUP BY FatherID, MotherID
    HAVING COUNT(*) > 1
)
ORDER BY FatherID, MotherID, FamilyID;