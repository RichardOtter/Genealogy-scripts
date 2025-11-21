-- database: ../../../../../Genealogy/GeneDB/Otter-Saito.rmtree

INSERT OR IGNORE INTO DNATableExtra (SupRecID, Sort1)
SELECT DNATable.RecID, cast(round(SharedCM, 2) *10 as INT)
FROM DNATable;


SELECT ROW_NUMBER() OVER( ORDER BY Sort1 DESC, Sort2 ASC)AS Num,
    dt.recID, Label2, dte.Sort1, Sort2, dte.Info, dt.rowid, dte.rowid
FROM DNATable as dt
INNER JOIN rde.DNATableExtra AS dte ON dt.RecID = dte.SupRecID
WHERE dt.DNAProvider = 2
--AND Sort1 = 190
AND ID1 = 17
ORDER BY Sort1 DESC, Sort2 ASC;