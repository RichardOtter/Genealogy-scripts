DROP VIEW IF EXISTS LU_ColorCodeSetName;

CREATE VIEW LU_ColorCodeSetName AS
WITH RECURSIVE
ColorSets AS (
    SELECT 0 AS ColorSetID
    UNION ALL
    SELECT ColorSetID + 1 FROM ColorSets WHERE ColorSetID < 9
),
xmlsrc AS (
    SELECT CAST(datarec AS TEXT) AS xml
    FROM configtable
    WHERE rowid = 1
),
Raw AS (
    SELECT
        cs.ColorSetID,
        xml_extract(
            (SELECT xml FROM xmlsrc),
            'Root/ColorCode' || cs.ColorSetID || '/Name/text()'
        ) AS RawName
    FROM ColorSets cs
),
Decoded AS (
    SELECT
        ColorSetID,
        REPLACE(
        REPLACE(
        REPLACE(
        REPLACE(
        REPLACE(RawName,
            '&amp;', '&'
        ),
            '&apos;', ''''
        ),
            '&quot;', '"'
        ),
            '&lt;', '<'
        ),
            '&gt;', '>'
        ) AS ColorSetName
    FROM Raw
)
SELECT
    ColorSetID,
    ColorSetName
FROM Decoded
WHERE ColorSetName IS NOT NULL
ORDER BY ColorSetID;
