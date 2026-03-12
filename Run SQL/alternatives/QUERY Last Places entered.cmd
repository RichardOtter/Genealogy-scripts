@ECHO OFF
ECHO The last nn places entered into RM
ECHO.
ECHO.
(
  echo   SELECT PlaceID,' ', Name
  echo   FROM PlaceTable
  echo   WHERE PlaceType = 0
  echo   ORDER BY PlaceID DESC
  echo   LIMIT 30;
  echo .quit
) | "C:\bin\SQLite\sqlite3" "C:\Users\rotter\Genealogy\GeneDB\Otter-Saito.rmtree"
ECHO.
ECHO.
pause
