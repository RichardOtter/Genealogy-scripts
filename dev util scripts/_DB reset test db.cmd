@ECHO OFF 
ECHO Reset the TEST database from the local backup copy

SET DB_EXTEN=rmtree
SET DB_BU_EXTEN=rmtreeBU
SET DEV_DB_PATH=.

REM Get the script folder name
SET DB_DIR=%cd%
cd ..
REM get current folder name
for %%I in (.) do set CurrDirName=%%~nxI
cd "%DB_DIR%"

SET DEV_DB_NAME=TEST-%CurrDirName%
SET DEV_DB_BACKUP=BACKUP_TEST-%CurrDirName%

REM delete existing dev test database
del "%DEV_DB_PATH%\%DEV_DB_NAME%.%DB_EXTEN%"

REM copy the local backup copy to the test DB name
copy "%DEV_DB_PATH%\%DEV_DB_BACKUP%.%DB_BU_EXTEN%" "%DEV_DB_PATH%\%DEV_DB_NAME%.%DB_EXTEN%"
CALL :CheckCopy "Creating local backup copy failed."

ECHO All copy operations completed successfully.
timeout -t 5
GOTO :EOF


:CheckCopy
REM %1 = error message
IF %ERRORLEVEL% NEQ 0 (
    ECHO.
    ECHO ERROR: %~1
    ECHO.
    PAUSE
    EXIT /B 1
)
EXIT /B 0