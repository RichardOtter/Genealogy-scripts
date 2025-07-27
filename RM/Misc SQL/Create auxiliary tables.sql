

INSERT INTO AuxMultimediaTable
VALUES (
13,
'e0072553a5c6d3f15529e9505a808c8f',
julianday('now') - 2415018.5
);





DROP TABLE main.AuxDNATable;
DROP TABLE main.AuxMultimediaTable;





ATTACH DATABASE
"C:\Users\rotter\Development\Genealogy\repo Genealogy-scripts\RM\Misc SQL\DB\RMDataExtra.sqlite"
AS adf;  -- auxiliary data file


CREATE TABLE main.AuxMultimediaTable (
AuxMultimediaTableID INTEGER PRIMARY KEY,
MD5Hash TEXT,
UTCModDate FLOAT,
FOREIGN KEY (AuxMultimediaTableID) REFERENCES MultimediaTable(MediaID)
    ON DELETE CASCADE
);


CREATE TABLE main.AuxDNATable (
AuxDNATableID INTEGER PRIMARY KEY,
Sort1 INTEGER,
Sort2 INTEGER,
UTCModDate FLOAT,
FOREIGN KEY (AuxDNATableID) REFERENCES DNATable(RecID)
    ON DELETE CASCADE
);
-- tested-  delete a row in dnatable, the corresponding row in aux dna table is dleted.
-- if dele row in aux dna table, nothing hppens in dnatable.

PRAGMA foreign_keys = OFF;

INSERT INTO main.AuxDNATable ( AuxDNATableID, Sort1, Sort2, UTCModDate)
SELECT SupRecID, Sort2, Sort2, julianday('now') - 2415018.5
FROM adf.DNATableExtra;

PRAGMA foreign_keys = ON;






--Had to turn off foreign foreign_key , why

Select RecID, AuxDNATableID
from AuxDNATable as adt
inner join DNATable on RecID = AuxDNATableID

--couldn't find nulls, or duplicates. turn on constraint ans it ok




--Backup the tables into an external file
--create empty DB
\bin\sqlite3 "C:\Users\rotter\Development\Genealogy\repo Genealogy-scripts\RM\Misc SQL\DB\BU RMDataExtra.sqlite"

-- do the backup
ATTACH DATABASE
"C:\Users\rotter\Development\Genealogy\repo Genealogy-scripts\RM\Misc SQL\DB\BU RMDataExtra.sqlite"
AS adf;  -- auxiliary data file

CREATE TABLE adf.newAuxDNATable AS SELECT * FROM main.AuxDNATable;

CREATE TABLE adf.AuxMultimediaTable AS SELECT * FROM main.AuxMultimediaTable;
