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
        /* Locate the <ColorCodeN> block */
        substr(
            (SELECT xml FROM xmlsrc),
            instr((SELECT xml FROM xmlsrc),
                  '<ColorCode' || cs.ColorSetID || '>') 
              + length('<ColorCode' || cs.ColorSetID || '>'),
            instr((SELECT xml FROM xmlsrc),
                  '</ColorCode' || cs.ColorSetID || '>')
              - (instr((SELECT xml FROM xmlsrc),
                       '<ColorCode' || cs.ColorSetID || '>')
                 + length('<ColorCode' || cs.ColorSetID || '>'))
        ) AS Block
    FROM ColorSets cs
),
NameExtract AS (
    SELECT
        ColorSetID,
        /* Extract <Name>...</Name> from inside the block */
        substr(
            Block,
            instr(Block, '<Name>') + length('<Name>'),
            instr(Block, '</Name>') - (instr(Block, '<Name>') + length('<Name>'))
        ) AS RawName
    FROM Raw
),
Decoded AS (
    SELECT
        ColorSetID,
        /* Decode XML entities */
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
    FROM NameExtract
)
SELECT
    ColorSetID,
    ColorSetName
FROM Decoded
WHERE ColorSetName IS NOT NULL
ORDER BY ColorSetID;
