WITH Constants AS (
    SELECT
        'GRP: Died before age 10' AS GroupName,
        'Died_Young.png'          AS RequiredFile
),

-- Identify the TagValue that defines the group
GroupID AS (
    SELECT TagValue
    FROM TagTable
    WHERE TagType = 0
      AND TagName COLLATE NOCASE = (SELECT GroupName FROM Constants)
),

-- Expand all StartID–EndID ranges into actual PersonIDs
GroupPeople AS (
    SELECT p.PersonID
    FROM PersonTable p
    JOIN GroupTable AS gt ON p.PersonID BETWEEN gt.StartID AND gt.EndID
    WHERE gt.GroupID = (SELECT TagValue FROM GroupID)
),

-- People in the group who DO have the required multimedia file
PeopleWithFile AS (
    SELECT DISTINCT ml.OwnerID AS PersonID
    FROM MediaLinkTable ml
    JOIN MultimediaTable m
        ON m.MediaID = ml.MediaID
    WHERE ml.OwnerType = 0
      AND ml.OwnerID IN (SELECT PersonID FROM GroupPeople)
      AND m.MediaFile COLLATE NOCASE = (SELECT RequiredFile FROM Constants)
),

-- People who need the file attached
PeopleNeedingFile AS (
    SELECT gp.PersonID
    FROM GroupPeople gp
    LEFT JOIN PeopleWithFile pwf
        ON pwf.PersonID = gp.PersonID
    WHERE pwf.PersonID IS NULL
),

-- Count matching media rows
MediaCount AS (
    SELECT
        COUNT(*) AS Cnt,
        MIN(MediaID) AS MediaID
    FROM MultimediaTable
    WHERE MediaFile COLLATE NOCASE = (SELECT RequiredFile FROM Constants)
),

-- Proceed only if exactly one match exists
Proceed AS (
    SELECT MediaID
    FROM MediaCount
    WHERE Cnt = 1
)

INSERT INTO MediaLinkTable (MediaID, OwnerType, OwnerID, IsPrimary, 
    Include1, Include2, Include3, Include4,
    SortOrder, 
    RectLeft, RectTop, RectRight, RectBottom, 
    Comments, UTCModDate)
SELECT
    (SELECT MediaID FROM Proceed),
    0 AS OwnerType,
    pnf.PersonID,
    1 AS IsPrimary,
    0 AS Include1, 0 AS Include2, 0 AS Include3, 0 AS Include4,
    0 AS SortOrder,
    0 AS RectLeft, 0 AS RectTop, 0 AS RectRight, 0 AS RectBottom,
    '' AS Comments, julianday('now') - 2415018.5
FROM PeopleNeedingFile pnf
JOIN Proceed ON 1 = 1;
