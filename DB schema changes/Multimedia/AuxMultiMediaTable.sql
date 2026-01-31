-- Not yet in use
-- Consider how know updates to external files should be handled
-- what happens if a mismatch is detected
-- a date that the hash was created would be good.
-- hash column should not be named md5, perhaps another column will have type
-- need a trigger for when a new row is added ??? to main table
-- foreign key constraint will delete the row in the aux table when the matching
-- row in main table is deleted

--  AuxMultimediaTable
CREATE TABLE IF NOT EXISTS AuxMultimediaTable (
AuxMediaID INTEGER PRIMARY KEY,
FileSize INTEGER,
FileTimeCreation FLOAT,
FileTimeModification FLOAT,
HashType TEXT,
Hash TEXT,
UTCModDate FLOAT,
FOREIGN KEY (AuxMediaID) REFERENCES MultimediaTable(MediaID)
    ON DELETE CASCADE
);

--  AuxMultimediaTable trigger
CREATE TRIGGER IF NOT EXISTS AuxMultimediaTable_UTCModDate
AFTER UPDATE ON AuxMultimediaTable
FOR EACH ROW
BEGIN
  UPDATE AuxMultimediaTable
  SET UTCModDate = julianday('now') - 2415018.5
  WHERE rowid = NEW.rowid;
END;



INSERT INTO AuxMultimediaTable
VALUES (
14,
'MD5',
'e0072553a5c6d3f15529e9505a808c8f',
julianday('now') - 2415018.5 - 1300,
julianday('now') - 2415018.5 - 1000,
julianday('now') - 2415018.5
);


