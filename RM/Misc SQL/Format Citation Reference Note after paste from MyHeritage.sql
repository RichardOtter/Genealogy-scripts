
-- Script to format the ActualText (Reference Note) in the CitationTable
-- after doing a full page copy and plain-text paste from a MyHeritage profile
-- web page to the RM Note editor.
-- Only the first , fourth and last Updates in this script delete text from the note.

-- TODO
-- ONLY OPERATE ON MYhER RECORDS
-- confirm that each note has only one instance of the keywords- Facts, Immediate family etc.
-- confirm proper handling for the different tree permissions- member, editor non-member
--  put date in a CTE at top

--delete initial stuff
UPDATE  CitationTable
SET ActualText= regexp_replace(
    ActualText,
    '(?s)\A.*(Edit profile|View in tree)(\r\n)+',
    '')
WHERE  regexp_like(ActualText, 'Details\r\nMatches\r\n' )
    AND NOT ActualText LIKE '%\_AUTOEDIT%' ESCAPE '\';


--divide at Facts
UPDATE  CitationTable
SET ActualText= regexp_replace(
    ActualText,
    'Facts\r\n(\r\nAdd\r\n)*',
    '\r\n===========================================DIV50==\r\nFacts\r\n\r\n')
WHERE  regexp_like(ActualText, 'Details\r\nMatches\r\n' )
    AND NOT ActualText LIKE '%\_AUTOEDIT%' ESCAPE '\';



-- divide at Details/Matches
UPDATE  CitationTable
SET ActualText= regexp_replace(
    ActualText, 
    '\Details\r\nMatches',
    '\r\n===========================================DIV50==\r\nDetails\r\nMatches')
WHERE  regexp_like(ActualText, 'Details\r\nMatches\r\n' )
    AND NOT ActualText LIKE '%\_AUTOEDIT%' ESCAPE '\';


-- divide at on the map
UPDATE  CitationTable
SET ActualText= regexp_replace(
    ActualText, 
    '\r\n.*?journey\r\n(.*\r\n)*.*on the map(\.)*\r\n',
    '\r\n\r\n\r\n')
WHERE  regexp_like(ActualText, 'Details\r\nMatches\r\n' )
    AND NOT ActualText LIKE '%\_AUTOEDIT%' ESCAPE '\';


-- divide at Immediate family
UPDATE  CitationTable
SET ActualText= regexp_replace(
    ActualText, 
    '\r\nImmediate family\r\n(\r\nAdd\r\n)*',
    '\r\n\r\n===========================================DIV50==\r\nImmediate family\r\n\r\n')
WHERE  regexp_like(ActualText, 'Details\r\nMatches\r\n' )
    AND NOT ActualText LIKE '%\_AUTOEDIT%' ESCAPE '\';


-- divide at Additional actions
UPDATE  CitationTable
SET ActualText= regexp_replace(
    ActualText, 
    '(?s)Additional actions\r\nPrint.*\z', 
    '\r\n===========================================DIV50==\r\n_AUTOEDIT-2025-11-19-01\r\n')
where regexp_like (ActualText, 'Details\r\nMatches\r\n')
    AND NOT ActualText LIKE '%\_AUTOEDIT%' ESCAPE '\';

-- close up blank lines 4>2
UPDATE  CitationTable
SET ActualText= regexp_replace(
    ActualText, 
    '\r\n\r\n\r\n\r\n', 
    '\r\n\r\n')
where regexp_like (ActualText, 'Details\r\nMatches\r\n');

-- close up blank lines 3>2
UPDATE  CitationTable
SET ActualText= regexp_replace(
    ActualText, 
    '\r\n\r\n\r\n', 
    '\r\n\r\n')
where regexp_like (ActualText, 'Details\r\nMatches\r\n');



-- check result
select ActualText
from CitationTable
where regexp_like (ActualText, 'Details\r\nMatches\r\n');


