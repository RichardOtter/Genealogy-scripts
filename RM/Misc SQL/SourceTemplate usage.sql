-- Number of sources that use the template
SELECT stt.TemplateID, stt.Name, COUNT(stt.TemplateID)
FROM SourceTemplateTable AS stt
INNER JOIN SourceTable AS st ON st.TemplateID=stt.TemplateID
GROUP BY stt.TemplateID
HAVING COUNT(*) > 0
ORDER BY COUNT(stt.TemplateID) DESC;

-- Number of citations that use the template
SELECT stt.TemplateID, stt.Name AS "Template Name", COUNT(stt.TemplateID) AS "# of citations"
FROM SourceTemplateTable AS stt
INNER JOIN SourceTable AS st ON st.TemplateID=stt.TemplateID
INNER JOIN CitationTable AS ct ON ct.SourceID = st.SourceID
GROUP BY stt.TemplateID
HAVING COUNT(*) > 0
ORDER BY COUNT(stt.TemplateID) DESC;

-- List the sources that use a particular template (by ID)
SELECT st.NAME
FROM SourceTable AS st
WHERE st.TemplateID=?;
