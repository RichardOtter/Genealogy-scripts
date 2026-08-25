BEGIN TRANSACTION;

UPDATE PlaceTable
SET Name = (SELECT FS_NameFull_en FROM AuxPlaceTable a
            WHERE a.PlaceID = PlaceTable.PlaceID),
    Abbrev = (SELECT FS_Abbrev FROM AuxPlaceTable a
              WHERE a.PlaceID = PlaceTable.PlaceID),
    Normalized = (SELECT FS_NameFull_en FROM AuxPlaceTable a
                  WHERE a.PlaceID = PlaceTable.PlaceID),
    Latitude = (SELECT FS_Latitude FROM AuxPlaceTable a
                WHERE a.PlaceID = PlaceTable.PlaceID),
    Longitude = (SELECT FS_Longitude FROM AuxPlaceTable a
                 WHERE a.PlaceID = PlaceTable.PlaceID),
    LatLongExact = 1
WHERE PlaceID IN (
    SELECT PlaceID FROM AuxPlaceTable
    WHERE FS_Status = 'ready'
      AND FS_NameFull_en IS NOT NULL
);

COMMIT;