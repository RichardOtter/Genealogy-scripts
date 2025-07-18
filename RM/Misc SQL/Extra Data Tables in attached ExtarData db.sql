
-- Create the RmDataExtra.sqlite  file/database using command line-
--     sqlite3 RmDataExtra.sqlite

-- Seems that SQLite Expert cannot run SQL without an open database
-- cannot do the attach as main, but opening the DB automatically calls it main

ATTACH DATABASE  
'C:\Users\rotter\Development\Genealogy\repo Genealogy-scripts\RM\Misc SQL\DB\TEST-Misc SQL.rmtree'
AS main;

ATTACH DATABASE
'C:\Users\rotter\Development\Genealogy\repo Genealogy-scripts\RM\Misc SQL\DB\RmDataExtra.sqlite'
AS rde; 

CREATE TABLE rde.DNATableExtra (
SupRecID INTEGER PRIMARY KEY,
Sort TEXT,
Info TEXT
);

-- in SQLite Expert, look in Table list for table "rde.DNATableExtra"
-- General settings pref determines whether it is in main list or separated by DB name

-- Display DNA Table and Extra data in grid
SELECT Label1, Label2, Info
FROM DNATable as dt
INNER JOIN rde.DNATableExtra AS dte ON dt.RecID = dte.RecID;



--===========================================DIV50==
-- testing


ATTACH DATABASE  
'C:\Users\rotter\Development\Genealogy\repo Genealogy-scripts\RM\Misc SQL\DB\TEST-Misc SQL.rmtree'
AS main;

SELECT Label1, Label2
FROM DNATable as dt
WHERE dt.recId = 7;

ATTACH DATABASE
'C:\Users\rotter\Development\Genealogy\repo Genealogy-scripts\RM\Misc SQL\DB\RmDataExtra.sqlite'
AS rde; 

CREATE TABLE rde.DNATableExtra (
SupRecID INTEGER PRIMARY KEY,
RecID INTEGER,
Info TEXT
);

INSERT INTO rde.DNATableExtra AS dte
VALUES (1,7,'Info test');

SELECT *
FROM rde.DNATableExtra as dte
WHERE dte.recId = 7;

SELECT Label1, Label2
FROM DNATable as dt
WHERE dt.recId = 7;

-- Display DNA Table and Extra data in grid
SELECT Label1, Label2, Sort, Info
FROM DNATable as dt
INNER JOIN rde.DNATableExtra AS dte ON dt.RecID = dte.RecID
WHERE dt.recId = 5;



DROP TABLE DNATableExtra;

CREATE TABLE rde.DNATableExtra (
SupRecID INTEGER PRIMARY KEY,
RecID INTEGER,
Sort1 INTEGER,
Sort2 INTEGER,
Info TEXT
);

-- remove all rows
DELETE FROM rde.DNATableExtra;




DNAProvider
1   23andMe
2   Ancestry.com
3
4
5   myHeritage

-- Add more rows to Extra table after new DNATable entries were made.
INSERT OR IGNORE INTO DNATableExtra (SupRecID, Sort1)
SELECT DNATable.RecID, cast(round(SharedCM, 2) *10 as INT)
FROM DNATable;

-- Fix order   (be sure to specify record ID, not row number)
UPDATE DNATableExtra
SET Sort2 = 2
WHERE SupRecID = 1683;

SELECT ROW_NUMBER() OVER( ORDER BY Sort1 DESC, Sort2 ASC)AS Num,
    dt.recID, Label2, dte.Sort1, Sort2, dte.Info
FROM DNATable as dt
INNER JOIN rde.DNATableExtra AS dte ON dt.RecID = dte.SupRecID
WHERE dt.DNAProvider = 2
AND ID1 = 1
ORDER BY Sort1 DESC, Sort2 ASC;
