
ATTACH DATABASE  
'C:\Users\rotter\Development\Genealogy\repo Genealogy-scripts\RM\Misc SQL\DB\TEST-Misc SQL.rmtree'
AS main;

ATTACH DATABASE
'C:\Users\rotter\Development\Genealogy\repo Genealogy-scripts\RM\Misc SQL\DB\RmDataExtra.sqlite'
AS rde; 


CREATE TABLE rde.DnaTableExtra (
SupRecID INTEGER PRIMARY KEY,
RecID INTEGER,
Info TEXT
);

-- Display DNA Table and Extra data in grid
SELECT Label1, Label2, Info
FROM DnaTable as dt
INNER JOIN rde.DnaTableExtra AS dte ON dt.RecID = dte.RecID;



--===========================================DIV50==
-- testing


ATTACH DATABASE  
'C:\Users\rotter\Development\Genealogy\repo Genealogy-scripts\RM\Misc SQL\DB\TEST-Misc SQL.rmtree'
AS main;

SELECT Label1, Label2
FROM DnaTable as dt
WHERE dt.recId = 7;

ATTACH DATABASE
'C:\Users\rotter\Development\Genealogy\repo Genealogy-scripts\RM\Misc SQL\DB\RmDataExtra.sqlite'
AS rde; 



CREATE TABLE rde.DnaTableExtra (
SupRecID INTEGER PRIMARY KEY,
RecID INTEGER,
Info TEXT
);

INSERT INTO rde.DnaTableExtra AS dte
VALUES (1,7,'Info test');

SELECT *
FROM rde.DnaTableExtra as dte
WHERE dte.recId = 7;

SELECT Label1, Label2
FROM DnaTable as dt
WHERE dt.recId = 7;

-- Display DNA Table and Extra data in grid
SELECT Label1, Label2, Info
FROM DnaTable as dt
INNER JOIN rde.DnaTableExtra AS dte ON dt.RecID = dte.RecID
WHERE dt.recId = 7;
