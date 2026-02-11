
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


-- sample data
INSERT INTO AuxMultimediaTable
VALUES (
1477,
julianday('now') - 2415018.5 - 1300,
julianday('now') - 2415018.5 - 1000,
julianday('now') - 2415018.5,
'MD5',
'e0072553a5c6d3f15529e9505a808c8f'
);


