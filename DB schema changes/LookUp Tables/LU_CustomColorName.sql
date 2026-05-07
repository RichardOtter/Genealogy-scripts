
DROP VIEW IF EXISTS LU_CustomColorName;

CREATE VIEW IF NOT EXISTS LU_CustomColorName AS
WITH RECURSIVE
ColorSets AS (
    SELECT 0 AS ColorSetID
    UNION ALL
    SELECT ColorSetID + 1 FROM ColorSets WHERE ColorSetID < 9
),
FieldNames AS (
    SELECT 0 AS ColorID
    UNION ALL
    SELECT ColorID + 1 FROM FieldNames WHERE ColorID < 27
),
xmlsrc AS (
    SELECT CAST(datarec AS TEXT) AS xml
    FROM configtable
    WHERE rowid = 1
),
Extracted AS (
    SELECT
        cs.ColorSetID,
        fn.ColorID,
        xml_extract(
            (SELECT xml FROM xmlsrc),
            'Root/ColorCode' || cs.ColorSetID ||
            '/FieldName' || fn.ColorID || '/text()'
        ) AS CustomColorName
    FROM ColorSets cs
    CROSS JOIN FieldNames fn
)
SELECT
    ColorSetID,
    ColorID,
    CustomColorName
FROM Extracted
WHERE CustomColorName IS NOT NULL
ORDER BY ColorSetID, ColorID;
