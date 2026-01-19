WITH RECURSIVE

-- ==========================================================
-- RELATIONSHIP EDGES
-- ==========================================================
Edges AS (
    SELECT f.FatherID AS FromID, c.ChildID AS ToID, 'parent' AS Rel
    FROM FamilyTable f
    JOIN ChildTable c ON c.FamilyID = f.FamilyID
    WHERE f.FatherID IS NOT NULL

    UNION ALL
    SELECT f.MotherID, c.ChildID, 'parent'
    FROM FamilyTable f
    JOIN ChildTable c ON c.FamilyID = f.FamilyID
    WHERE f.MotherID IS NOT NULL

    UNION ALL
    SELECT c.ChildID, f.FatherID, 'child'
    FROM FamilyTable f
    JOIN ChildTable c ON c.FamilyID = f.FamilyID
    WHERE f.FatherID IS NOT NULL

    UNION ALL
    SELECT c.ChildID, f.MotherID, 'child'
    FROM FamilyTable f
    JOIN ChildTable c ON c.FamilyID = f.FamilyID
    WHERE f.MotherID IS NOT NULL

    UNION ALL
    SELECT f.FatherID, f.MotherID, 'spouse'
    FROM FamilyTable f
    WHERE f.FatherID IS NOT NULL AND f.MotherID IS NOT NULL

    UNION ALL
    SELECT f.MotherID, f.FatherID, 'spouse'
    FROM FamilyTable f
    WHERE f.FatherID IS NOT NULL AND f.MotherID IS NOT NULL
),

-- ==========================================================
-- BFS (DEPTH-LIMITED, SQLITE-LEGAL)
-- ==========================================================
Path AS (
    SELECT
        1 AS CurrentID,
        '1' AS PathIDs,
        '' AS PathRels,
        0 AS Depth

    UNION ALL

    SELECT
        e.ToID,
        Path.PathIDs || ',' || e.ToID,
        Path.PathRels || ',' || e.Rel,
        Path.Depth + 1
    FROM Path
    JOIN Edges e ON e.FromID = Path.CurrentID
    WHERE
        Path.Depth < 10
        AND ',' || Path.PathIDs || ',' NOT LIKE '%,' || e.ToID || ',%'
),

-- ==========================================================
-- SHORTEST PATH
-- ==========================================================
BestPath AS (
    SELECT *
    FROM Path
    WHERE CurrentID = 17
    ORDER BY Depth
    LIMIT 1
),

-- ==========================================================
-- SPLIT PathIDs SAFELY (NO JSON)
-- ==========================================================
SplitIDs AS (
    SELECT
        1 AS Step,
        CAST(substr(PathIDs, 1, instr(PathIDs || ',', ',') - 1) AS INTEGER) AS PersonID,
        substr(PathIDs || ',', instr(PathIDs || ',', ',') + 1) AS Rest
    FROM BestPath

    UNION ALL

    SELECT
        Step + 1,
        CAST(substr(Rest, 1, instr(Rest, ',') - 1) AS INTEGER),
        substr(Rest, instr(Rest, ',') + 1)
    FROM SplitIDs
    WHERE Rest <> ''
),

SplitRels AS (
    SELECT
        2 AS Step,
        substr(PathRels, 2, instr(substr(PathRels,2) || ',', ',') - 1) AS Rel,
        substr(substr(PathRels,2) || ',', instr(substr(PathRels,2) || ',', ',') + 1) AS Rest
    FROM BestPath

    UNION ALL

    SELECT
        Step + 1,
        substr(Rest, 1, instr(Rest, ',') - 1),
        substr(Rest, instr(Rest, ',') + 1)
    FROM SplitRels
    WHERE Rest <> ''
)

-- ==========================================================
-- FINAL OUTPUT
-- ==========================================================
SELECT
    i.Step,
    n.Given || ' ' || n.Surname AS Name,
    r.Rel AS Relationship
FROM SplitIDs i
JOIN NameTable n
    ON n.OwnerID = i.PersonID
   AND n.IsPrimary = 1
LEFT JOIN SplitRels r
    ON r.Step = i.Step
ORDER BY i.Step;
