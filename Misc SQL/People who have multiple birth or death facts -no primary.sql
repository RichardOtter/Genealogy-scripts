-- Find people who have multiple birth or death facts
-- and either set has no primary set.

SELECT  et.OwnerID, ftt.name, COUNT(*), SUM(isPrimary)
FROM eventtable et
INNER JOIN facttypetable as ftt on et.EventType = ftt.FactTypeID
WHERE ftt.name = 'Birth' 
OR ftt.name = 'Death'
GROUP BY ownerid, eventtype
HAVING COUNT(*) >2 AND SUM(isPrimary)=0;


