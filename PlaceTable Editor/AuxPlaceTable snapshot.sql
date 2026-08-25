BEGIN TRANSACTION;

INSERT OR IGNORE INTO AuxPlaceTable (
    PlaceID, Orig_PlaceType, Orig_Name, Orig_Abbrev, Orig_Normalized,
    Orig_Latitude, Orig_Longitude, Orig_LatLongExact, Orig_MasterID,
    Orig_Note, Orig_Reverse, Orig_fsID, Orig_anID, Orig_UTCModDate
)
SELECT PlaceID, PlaceType, Name, Abbrev, Normalized,
       Latitude, Longitude, LatLongExact, MasterID,
       Note, Reverse, fsID, anID, UTCModDate
FROM PlaceTable;

COMMIT;