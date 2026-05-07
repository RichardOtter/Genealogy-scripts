DROP VIEW IF EXISTS LU_CustomColorName;

CREATE VIEW LU_CustomColorName AS
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

/* Extract the entire <ColorCodeN>...</ColorCodeN> block */
Blocks AS (
    SELECT
        cs.ColorSetID,
        substr(
            xml,
            instr(xml, '<ColorCode' || cs.ColorSetID || '>')
              + length('<ColorCode' || cs.ColorSetID || '>'),
            instr(xml, '</ColorCode' || cs.ColorSetID || '>')
              - (instr(xml, '<ColorCode' || cs.ColorSetID || '>')
                 + length('<ColorCode' || cs.ColorSetID || '>'))
        ) AS Block
    FROM ColorSets cs
    CROSS JOIN xmlsrc
),

/* Extract <FieldNameN>...</FieldNameN> from inside each block */
Raw AS (
    SELECT
        b.ColorSetID,
        fn.ColorID,
        substr(
            b.Block,
            instr(b.Block, '<FieldName' || fn.ColorID || '>') 
              + length('<FieldName' || fn.ColorID || '>'),
            instr(b.Block, '</FieldName' || fn.ColorID || '>')
              - (instr(b.Block, '<FieldName' || fn.ColorID || '>')
                 + length('<FieldName' || fn.ColorID || '>'))
        ) AS RawName
    FROM Blocks b
    CROSS JOIN FieldNames fn
),

/* Decode XML named entities */
Decoded AS (
    SELECT
        ColorSetID,
        ColorID,
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
        ) AS CustomColorName
    FROM Raw
)

SELECT
    ColorSetID,
    ColorID,
    CustomColorName
FROM Decoded
WHERE CustomColorName IS NOT NULL
ORDER BY ColorSetID, ColorID;
