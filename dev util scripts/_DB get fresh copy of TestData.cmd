@ECHO OFF
ECHO Copy the test database to the local dev database folder

SET DB_EXTEN=rmtree
SET DB_BU_EXTEN=rmtreeBU

SET TEST_DB_PATH=C:\Users\rotter\dev\Genealogy\repo Genealogy-scripts\Test Data
SET TEST_DB_NAME=TestData-RMpython

SET DEV_DB_PATH=.

REM Get the script folder name
SET DB_DIR=%cd%
cd ..
REM get current folder name
for %%I in (.) do set CurrDirName=%%~nxI
cd "%DB_DIR%"

SET DEV_DB_NAME=TEST-%CurrDirName%
SET DEV_DB_BACKUP=BACKUP_TEST-%CurrDirName%

REM delete existing dev test database and local backup
del "%DEV_DB_PATH%\%DEV_DB_NAME%.%DB_EXTEN%"
del "%DEV_DB_PATH%\%DEV_DB_BACKUP%.%DB_BU_EXTEN%"

REM This is the only reference to the test database
REM ---- COPY TEST → DEV ----
copy "%TEST_DB_PATH%\%TEST_DB_NAME%.%DB_EXTEN%" ^
      "%DEV_DB_PATH%\%DEV_DB_NAME%.%DB_EXTEN%"
CALL :CheckCopy "Copying TEST DB to dev DB failed."

REM ---- COPY DEV → DEV BACKUP ----
copy "%DEV_DB_PATH%\%DEV_DB_NAME%.%DB_EXTEN%" ^
     "%DEV_DB_PATH%\%DEV_DB_BACKUP%.%DB_BU_EXTEN%"
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