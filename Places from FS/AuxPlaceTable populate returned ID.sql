BEGIN TRANSACTION;

UPDATE AuxPlaceTable
SET FS_ReturnedID = TRIM(
    SUBSTR(
        Orig_Note,
        INSTR(UPPER(Orig_Note), 'FSPID=') + 6,
        CASE
            WHEN INSTR(
                SUBSTR(Orig_Note, INSTR(UPPER(Orig_Note), 'FSPID=') + 6),
                CHAR(10)
            ) = 0
            THEN LENGTH(Orig_Note)
            ELSE INSTR(
                SUBSTR(Orig_Note, INSTR(UPPER(Orig_Note), 'FSPID=') + 6),
                CHAR(10)
            ) - 1
        END
    ),
    ' ' || CHAR(9) || CHAR(10) || CHAR(13)
)
WHERE INSTR(UPPER(Orig_Note), 'FSPID=') > 0;

COMMIT;