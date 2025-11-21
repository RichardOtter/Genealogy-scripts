-- AuxDNATable has RecID
-- this table is joined by DNATable
-- INNER JOIN rde.DNATableExtra AS dte ON dt.RecID = dte.SupRecID

-- database: ../../../../../Genealogy/GeneDB/Otter-Saito.rmtree

WITH
 Constants AS (SELECT
    1     AS C_Matcher,
     2     AS C_DnaService,
     NULL  AS C_cMonly        -- NULL or integer (cM * 10)
    )
SELECT ROW_NUMBER() OVER( ORDER BY Sort1 DESC, Sort2 ASC) AS Num,
    Label2, Sort1, Sort2, Label1, dt.rowid, adt.rowid
FROM DNATable as dt
INNER JOIN AuxDNATable AS adt ON dt.RecID = adt.AuxDNATableID
WHERE DNAProvider = (SELECT C_DnaService FROM Constants)
 AND ID1 = (SELECT C_Matcher FROM Constants)
 AND IIF((SELECT C_cMonly FROM Constants) is not NULL, Sort1 = (SELECT C_cMonly FROM Constants), true)
ORDER BY Sort1 DESC, Sort2 ASC, RecID ASC;


-- Look for duplicate Label 2 entries for a given person and DNAService
WITH
 Constants AS (SELECT
    17   AS C_Matcher,
     2   AS C_DnaService),
 Duplicates(RecID, Label2, c) AS (
  SELECT RecID, Label2, COUNT(*) AS c
  FROM DNATable
  WHERE ID1=(SELECT C_Matcher FROM Constants)
    AND DNAProvider=(SELECT C_DnaService FROM Constants)
  GROUP BY Label2   --, SharedCM
  HAVING c >1
  ORDER BY SharedCM DESC)
SELECT RecID, Label2 from Duplicates;

-- TODO
-- look for duplicates
-- remove unmatched lines.Constants\
-- update DNATableExtra with new data