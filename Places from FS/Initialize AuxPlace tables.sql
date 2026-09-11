PRAGMA foreign_keys = ON;

BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS AuxPlaceTable (
    PlaceID INTEGER PRIMARY KEY,
    Orig_PlaceType INTEGER,
    Orig_Name TEXT,
    Orig_Abbrev TEXT,
    Orig_Normalized TEXT,
    Orig_Latitude INTEGER,
    Orig_Longitude INTEGER,
    Orig_LatLongExact INTEGER,
    Orig_MasterID INTEGER,
    Orig_Note TEXT,
    Orig_Reverse TEXT,
    Orig_fsID INTEGER,
    Orig_anID INTEGER,
    Orig_UTCModDate FLOAT,
    Language TEXT,
    Uncertain TEXT,
    FSPDesID INTEGER,
    FSPID INTEGER,
    NonFSPlace TEXT,
    FS_NameFull_en TEXT,
    FS_NameShort_en TEXT,
    FS_NameFull_de TEXT,
    FS_NameShort_de TEXT,
    FS_Abbrev TEXT,
    FS_Latitude INTEGER,
    FS_Longitude INTEGER,
    FS_YearStart INTEGER,
    FS_YearEnd INTEGER,
    FS_PlaceType TEXT,
    FS_PlaceStatus TEXT,
    FS_ParentID TEXT,
    FSMatchScore INTEGER,
    FS_LastUpdated FLOAT,
    FS_Status TEXT,
    FS_Error TEXT,
    FOREIGN KEY (PlaceID) REFERENCES PlaceTable(PlaceID) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_AuxPlaceTable_fsID
    ON AuxPlaceTable (Orig_fsID);

CREATE TABLE IF NOT EXISTS LU_FSPlaceTypes (
    FS_PlaceTypeID INTEGER PRIMARY KEY,
    EnglishName TEXT NOT NULL,
    TypeURL TEXT NOT NULL UNIQUE,
    LastUpdated FLOAT
);

-- Populate the place snapshot only when it is empty. FSPDesID is the
-- FamilySearch place-description ID extracted from PlaceTable.Note.
WITH PlaceSnapshot AS (
    SELECT
        PlaceID, PlaceType, Name, Abbrev, Normalized,
        Latitude, Longitude, LatLongExact, MasterID,
        Note, Reverse, fsID, anID, UTCModDate,
        REPLACE(Note, CHAR(13), '') AS CleanNote
    FROM PlaceTable
), FSPDesIDMarker AS (
    SELECT
        *,
        INSTR(UPPER(CleanNote), 'FSPID=') AS MarkerPosition
    FROM PlaceSnapshot
), FSPDesIDText AS (
    SELECT
        *,
        CASE
            WHEN MarkerPosition > 0 THEN TRIM(
                SUBSTR(
                    CleanNote,
                    MarkerPosition + 6,
                    INSTR(
                        SUBSTR(CleanNote || CHAR(10), MarkerPosition + 6),
                        CHAR(10)
                    ) - 1
                ),
                ' ' || CHAR(9)
            )
        END AS FSPDesIDValue
    FROM FSPDesIDMarker
)
INSERT INTO AuxPlaceTable (
    PlaceID, Orig_PlaceType, Orig_Name, Orig_Abbrev, Orig_Normalized,
    Orig_Latitude, Orig_Longitude, Orig_LatLongExact, Orig_MasterID,
    Orig_Note, Orig_Reverse, Orig_fsID, Orig_anID, Orig_UTCModDate,
    FSPDesID
)
SELECT
    PlaceID, PlaceType, Name, Abbrev, Normalized,
    Latitude, Longitude, LatLongExact, MasterID,
    Note, Reverse, fsID, anID, UTCModDate,
    CAST(FSPDesIDValue AS INTEGER)
FROM FSPDesIDText
WHERE NOT EXISTS (SELECT 1 FROM AuxPlaceTable);

COMMIT;
