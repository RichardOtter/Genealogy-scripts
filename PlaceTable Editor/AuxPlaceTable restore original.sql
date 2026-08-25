BEGIN TRANSACTION;

UPDATE PlaceTable
SET PlaceType = (SELECT Orig_PlaceType FROM AuxPlaceTable a
                 WHERE a.PlaceID = PlaceTable.PlaceID),
    Name = (SELECT Orig_Name FROM AuxPlaceTable a
            WHERE a.PlaceID = PlaceTable.PlaceID),
    Abbrev = (SELECT Orig_Abbrev FROM AuxPlaceTable a
              WHERE a.PlaceID = PlaceTable.PlaceID),
    Normalized = (SELECT Orig_Normalized FROM AuxPlaceTable a
                  WHERE a.PlaceID = PlaceTable.PlaceID),
    Latitude = (SELECT Orig_Latitude FROM AuxPlaceTable a
                WHERE a.PlaceID = PlaceTable.PlaceID),
    Longitude = (SELECT Orig_Longitude FROM AuxPlaceTable a
                 WHERE a.PlaceID = PlaceTable.PlaceID),
    LatLongExact = (SELECT Orig_LatLongExact FROM AuxPlaceTable a
                    WHERE a.PlaceID = PlaceTable.PlaceID),
    MasterID = (SELECT Orig_MasterID FROM AuxPlaceTable a
                WHERE a.PlaceID = PlaceTable.PlaceID),
    Note = (SELECT Orig_Note FROM AuxPlaceTable a
            WHERE a.PlaceID = PlaceTable.PlaceID),
    Reverse = (SELECT Orig_Reverse FROM AuxPlaceTable a
               WHERE a.PlaceID = PlaceTable.PlaceID),
    fsID = (SELECT Orig_fsID FROM AuxPlaceTable a
            WHERE a.PlaceID = PlaceTable.PlaceID),
    anID = (SELECT Orig_anID FROM AuxPlaceTable a
            WHERE a.PlaceID = PlaceTable.PlaceID),
    UTCModDate = (SELECT Orig_UTCModDate FROM AuxPlaceTable a
                  WHERE a.PlaceID = PlaceTable.PlaceID)
WHERE PlaceID IN (SELECT PlaceID FROM AuxPlaceTable);

COMMIT;