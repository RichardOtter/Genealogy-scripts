
REM Production
REM set DB_PATH=C:\\Users\\rotter\\Genealogy\\GeneDB\\Otter-Saito.rmtree
REM Test DB
set DB_PATH=../DB/TEST-DB schema changes.rmtree


REM create
set script_file=/Users/rotter/dev/Genealogy/repo Genealogy-scripts/DB schema changes/Logging/generated/_logging_trigger_full.sql

REM drop
REM set script_file=/Users/rotter/dev/Genealogy/repo Genealogy-scripts/DB schema changes/Logging/generated/_logging_trigger_drop.sql




REM TEST
REM set script_file=test.sql


sqlite3 "%DB_PATH%" < "%script_file%"


pause