select datetime(ChangeTime + 2415018.5, 'localtime'), *
from AuxChangeLog
order by ChangeLogID desc
limit 100;