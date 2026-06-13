select placeid, note
from placetable
where not note = ''
and regexp_like( note, '\d\d\d\d\d')
and not note like '%FSPID=%';
