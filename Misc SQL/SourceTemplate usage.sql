

-- List source templates, sort by the number of uses
-- does not include unused builtin templates
SELECT format('%-8u  %-5u      %!s', stt.TemplateID, COUNT(st.SourceID), stt.Name)
FROM  SourceTemplateTable AS stt
LEFT JOIN  SourceTable AS st ON st.TemplateID = stt.TemplateID
GROUP BY stt.TemplateID, stt.Name COLLATE NOCASE
HAVING NOT (stt.TemplateID < 1000 AND COUNT(st.SourceID) = 0)
ORDER BY COUNT(st.SourceID) DESC, stt.Name COLLATE NOCASE ASC;



-- Number of citations that use the template
SELECT format('%7u %7u  %s', stt.TemplateID, COUNT(stt.TemplateID), stt.Name)
FROM SourceTemplateTable AS stt
INNER JOIN SourceTable AS st ON st.TemplateID=stt.TemplateID
INNER JOIN CitationTable AS ct ON ct.SourceID = st.SourceID
GROUP BY stt.TemplateID
HAVING COUNT(*) > 0
ORDER BY COUNT(stt.TemplateID) DESC;


-- List all sources along with its template
SELECT format('%!-75s %!s', st.Name, stt.Name)
FROM SourceTable AS st 
INNER JOIN SourceTemplateTable AS stt ON st.TemplateID=stt.TemplateID
ORDER BY st.Name COLLATE NOCASE ASC


-- List the sources that use a particular template (by ID)
SELECT st.NAME
FROM SourceTable AS st
WHERE st.TemplateID=?;


-- Another template usage query
-- but does not show templates not in use.
-- Number of sources that use each used template
-- Lists Source Templates and the number of sources that use it
SELECT format("%8u    %4u      %s", stt.TemplateID, COUNT(stt.TemplateID), stt.Name)
FROM SourceTemplateTable AS stt
INNER JOIN SourceTable AS st ON st.TemplateID=stt.TemplateID
GROUP BY stt.TemplateID
HAVING COUNT(*) > 0
ORDER BY COUNT(stt.TemplateID) DESC;

