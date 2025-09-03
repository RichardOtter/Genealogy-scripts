-- AuxDNATable has RecID
-- this table is joined by DNATable
-- INNER JOIN rde.DNATableExtra AS dte ON dt.RecID = dte.SupRecID

-- database: ../../../../../Genealogy/GeneDB/Otter-Saito.rmtree



INSERT OR IGNORE INTO AuxDNATable (SupRecID, Sort1)
SELECT DNATable.RecID, cast(round(SharedCM, 2) *10 as INT)
FROM DNATable;


--  1       Richard
--  4       Rose
--  17      Roman
--  12      Ethel
--  6       Gloria
--  1530    Tamara

--  1       23andMe
--  2       Ancestry
--  5       MyHeritage


WITH
 Constants AS (SELECT
    17     AS C_Matcher,
     2     AS C_DnaService,
     1170  AS C_cMonly        -- NULL or integer (cM*10)
    )
SELECT ROW_NUMBER() OVER( ORDER BY Sort1 DESC, Sort2 ASC) AS Num,
    Label2, dte.Sort1, Sort2, dte.Info, Label1, dt.rowid, dte.rowid
FROM DNATable as dt
INNER JOIN rde.DNATableExtra AS dte ON dt.RecID = dte.SupRecID
WHERE dt.DNAProvider = (SELECT C_DnaService FROM Constants)
 AND IIF((SELECT C_cMonly FROM Constants) is not NULL, Sort1 = (SELECT C_cMonly FROM Constants), true)
ORDER BY Sort1 DESC, Sort2 ASC;


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