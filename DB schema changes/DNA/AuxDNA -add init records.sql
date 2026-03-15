-- database: c:\Users\rotter\Genealogy\GeneDB\Otter-Saito.rmtree

-- ======================================================================DIV80==
-- Create the table and trigger and then create rows in AuxDNATable 
-- corresponding to any existing rows in DNATable

CREATE TABLE AuxDNATable (
AuxDNATableID INTEGER PRIMARY KEY,
Sort1 INTEGER,
Sort2 INTEGER,
Info TEXT,
UTCModDate FLOAT,
FOREIGN KEY (AuxDNATableID) REFERENCES DNATable(RecID)
    ON DELETE CASCADE
);

CREATE TRIGGER IF NOT EXISTS AuxDNATable_UTCModDate
AFTER UPDATE ON AuxDNATable
FOR EACH ROW
BEGIN
  UPDATE AuxDNATable
  SET UTCModDate = julianday('now') - 2415018.5
  WHERE rowid = NEW.rowid;
END;

-- ======================================================================DIV80==

-- Sort1 is always generated automatically and based on SharedCM
-- Sort2 is adjusted manually to fix the displayed sort order
-- usually the set of matches with the same Sort1 value are all adjusted
-- with values 10 and up. This allows inserts for new records.

-- Info general information about the match that may be used in future
-- to display, ORDER BY by Sort1 ASC, Sort2 ASC

-- tested
-- delete a row in dnatable, the corresponding row in aux dna table is deleted.
-- if delete row in aux dna table, nothing happens in dnatable.
-- add a row to DNATable from RM, a corresponding AuxDNATable row is created.

INSERT OR IGNORE INTO AuxDNATable
(AuxDNATableID, Sort1, Sort2, Info, UTCModDate)
SELECT
  RecID,
  cast(round(SharedCM, 2) *10 as INT),
  0,
  null,
  julianday('now') - 2415018.5
FROM DNATable;

