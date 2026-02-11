-- Script to format the ActualText (Reference Note) in the CitationTable
-- after doing a full page copy and plain-text paste from a MyHeritage profile
-- web page to the RM Note editor.

-- TODO
-- confirm that each note has only one instance of the keywords- Facts, Immediate family etc.
-- confirm proper handling for the different tree permissions- member, editor non-member
-- help  https://regex101.com/


CREATE TABLE IF NOT EXISTS AuxCitationTable (
AuxCitationID INTEGER PRIMARY KEY,
SavedActualText TEXT,
UTCModDate FLOAT,
FOREIGN KEY (AuxCitationID) REFERENCES CitationTable(CitationID)
    ON DELETE CASCADE
);

DROP VIEW IF EXISTS Unmod_Citations_to_MyHr;

CREATE TEMP VIEW Unmod_Citations_to_MyHr AS
SELECT CitationID
FROM CitationTable AS ct
INNER JOIN SourceTable AS st ON ct.SourceID = st.SourceID
WHERE st.Name LIKE 'RRdb MYH%' COLLATE NOCASE
AND ct.ActualText NOT LIKE '%\_AUTOEDIT-2026-02-10-01%' ESCAPE '\';


-- save original note text
INSERT OR IGNORE INTO AuxCitationTable (AuxCitationID, SavedActualText, UTCModDate)
SELECT CitationID, ActualText, UTCModDate
FROM CitationTable
WHERE  CitationID IN (SELECT CitationID FROM Unmod_Citations_to_MyHr);


--delete initial stuff
UPDATE  CitationTable
SET ActualText= regexp_replace(
    ActualText,
    '(?s)\A.*(Edit profile|View in tree)(\r\n)+',
    '')
WHERE  CitationID IN (SELECT CitationID FROM Unmod_Citations_to_MyHr);


--divide at Facts
UPDATE  CitationTable
SET ActualText= regexp_replace(
    ActualText,
    'Facts(\r\n)+(Add\r\n)?',
    '\r\n===========================================DIV50==\r\nFacts\r\n\r\n')
WHERE  CitationID IN (SELECT CitationID FROM Unmod_Citations_to_MyHr);



-- divide at Details/Matches
UPDATE  CitationTable
SET ActualText= regexp_replace(
    ActualText, 
    '\Details\r\nMatches',
    '\r\n===========================================DIV50==\r\nDetails\r\nMatches')
WHERE  CitationID IN (SELECT CitationID FROM Unmod_Citations_to_MyHr);


-- divide at on the map
UPDATE  CitationTable
SET ActualText= regexp_replace(
    ActualText, 
    '\r\n.*?journey\r\n(.*\r\n)*.*on the map(\.)*\r\n',
    '\r\n\r\n\r\n')
WHERE  CitationID IN (SELECT CitationID FROM Unmod_Citations_to_MyHr);

-- divide at saved record
UPDATE  CitationTable
SET ActualText= regexp_replace(
    ActualText, 
    '\r\n(One|\d*) saved records?\r\n',
    '\r\n\r\n===========================================DIV50==\r\nSaved source records\r\n\r\n')
WHERE  CitationID IN (SELECT CitationID FROM Unmod_Citations_to_MyHr);


-- divide at Immediate family
UPDATE  CitationTable
SET ActualText= regexp_replace(
    ActualText, 
    
    '\r\nImmediate family(\r\n)+(Add\r\n)?',
    '\r\n\r\n===========================================DIV50==\r\nImmediate family\r\n\r\n')
WHERE  CitationID IN (SELECT CitationID FROM Unmod_Citations_to_MyHr);


-- divide at end part
UPDATE  CitationTable
SET ActualText= regexp_replace(
    ActualText, 
    '(?s)(Additional actions|Family tree\r\nGenealogy).*\z', 
    '\r\n===========================================DIV50==\r\n_AUTOEDIT-2026-02-10-01\r\n')
WHERE  CitationID IN (SELECT CitationID FROM Unmod_Citations_to_MyHr);


-- close up blank lines 4>2
UPDATE  CitationTable
SET ActualText= regexp_replace(
    ActualText, 
    '\r\n\r\n\r\n\r\n', 
    '\r\n\r\n')
WHERE  CitationID IN (SELECT CitationID FROM Unmod_Citations_to_MyHr);

-- close up blank lines 3>2
UPDATE  CitationTable
SET ActualText= regexp_replace(
    ActualText, 
    '\r\n\r\n\r\n', 
    '\r\n\r\n')
WHERE  CitationID IN (SELECT CitationID FROM Unmod_Citations_to_MyHr);



-- check result, show all MyHr citations
SELECT ct.CitationID, ct.CitationName, ct.ActualText
FROM CitationTable AS ct
INNER JOIN SourceTable AS st ON ct.SourceID = st.SourceID
WHERE st.Name LIKE 'RRdb MYH%' COLLATE NOCASE;



-- REVERT BACK

-- restore saved citation note to CitationTable
UPDATE CitationTable 
SET ActualText = SavedActualText
FROM AuxCitationTable 
WHERE  CitationID = AuxCitationID;

-- check result, show all MyHr citations
SELECT ct.CitationID, ct.CitationName, ct.ActualText
FROM CitationTable AS ct
INNER JOIN SourceTable AS st ON ct.SourceID = st.SourceID
WHERE st.Name LIKE 'RRdb MYH%' COLLATE NOCASE;


