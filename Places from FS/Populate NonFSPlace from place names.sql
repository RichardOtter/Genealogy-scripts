BEGIN TRANSACTION;

-- Classify name formats that require special handling during FamilySearch lookup.
-- Existing NonFSPlace values are preserved.
WITH CleanNames AS (
    SELECT
        PlaceID,
        Orig_Name,
        CASE
            WHEN INSTR(Orig_Name, '[') > 0
                AND INSTR(SUBSTR(Orig_Name, INSTR(Orig_Name, '[')), ']') > 0
                THEN SUBSTR(Orig_Name, 1, INSTR(Orig_Name, '[') - 1)
                    || SUBSTR(
                        Orig_Name,
                        INSTR(Orig_Name, '[')
                            + INSTR(
                                SUBSTR(Orig_Name, INSTR(Orig_Name, '[')), ']'
                            )
                    )
            ELSE Orig_Name
        END AS CleanName
    FROM AuxPlaceTable
), NameLevels AS (
    SELECT
        PlaceID,
        Orig_Name,
        TRIM(SUBSTR(CleanName, 1, INSTR(CleanName || ',', ',') - 1))
            AS FirstLevel,
        SUBSTR(CleanName || ',', INSTR(CleanName || ',', ',') + 1)
            AS RemainingLevels
    FROM CleanNames
), FirstTwoLevels AS (
    SELECT
        PlaceID,
        Orig_Name,
        FirstLevel,
        TRIM(SUBSTR(RemainingLevels, 1, INSTR(RemainingLevels, ',') - 1))
            AS SecondLevel
    FROM NameLevels
), NonFSFlags AS (
    SELECT
        PlaceID,
        NULLIF(TRIM(
            CASE
                WHEN INSTR(Orig_Name, '[') > 0
                    AND INSTR(Orig_Name, ']') > INSTR(Orig_Name, '[')
                    THEN '_BRACKET-TEXT;'
                ELSE ''
            END ||
            CASE
                WHEN FirstLevel <> ''
                    AND LOWER(FirstLevel) = LOWER(SecondLevel)
                    THEN '_GEMEINDE-ISSUE;'
                ELSE ''
            END ||
            CASE
                WHEN INSTR(UPPER(FirstLevel), 'COUNTY') > 0
                    THEN '_COUNTY;'
                ELSE ''
            END,
            ';'
        ), '') AS FlagValue
    FROM FirstTwoLevels
)
UPDATE AuxPlaceTable
SET NonFSPlace = (
    SELECT FlagValue
    FROM NonFSFlags
    WHERE NonFSFlags.PlaceID = AuxPlaceTable.PlaceID
)
WHERE NULLIF(TRIM(NonFSPlace), '') IS NULL
    AND EXISTS (
        SELECT 1
        FROM NonFSFlags
        WHERE NonFSFlags.PlaceID = AuxPlaceTable.PlaceID
            AND FlagValue IS NOT NULL
    );

COMMIT;
