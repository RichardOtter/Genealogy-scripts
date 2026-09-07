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
    NonFSPlace TEXT,
    FSPDesID INTEGER,
    FSPID INTEGER,
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

-- Language TEXT,
--   en or de  the lanugyaes are separate this shows which oto use ??
-- Uncertain TEXT,
--      flag if name has ~/_PROBABLY, ?/_UNCLEAR, _REGION, or _VICINITY
-- FSPDesID INTEGER,
--      FS Place description ID  The ID on web page
-- FSPID INTEGER,
--      FS Place ID
-- NonFSPlace TEXT,
--      forgot ???
-- FS_NameFull TEXT,
-- FS_NameShort TEXT,
-- FS_Abbrev TEXT,

-- FS_Latitude INTEGER,
-- FS_Longitude INTEGER,
-- FS_YearStart INTEGER,
-- FS_YearEnd INTEGER,

-- FS_PlaceType TEXT,
-- FS_PlaceStatus TEXT,

-- FS_ParentID TEXT,

-- FSMatchScore INTEGER, -- accepted lookup score
-- FS_LastUpdated FLOAT,
-- FS_Status TEXT,
-- FS_Error TEXT,
