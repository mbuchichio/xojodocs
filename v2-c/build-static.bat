@echo off
REM Static build with embedded SQLite (no external dependencies)
REM Download SQLite amalgamation from: https://www.sqlite.org/download.html

echo Building XojoDoc v2.0 (Static build with embedded SQLite)...
echo.

REM Check if sqlite3.c exists
if not exist "sqlite3.c" (
    echo ERROR: sqlite3.c not found!
    echo.
    echo Download SQLite amalgamation from:
    echo https://www.sqlite.org/download.html
    echo.
    echo Look for: sqlite-amalgamation-XXXXXXX.zip
    echo Extract sqlite3.c and sqlite3.h to this directory
    echo.
    exit /b 1
)

REM Check for GCC
where gcc >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: GCC not found!
    echo Please install MinGW-w64 or use MSYS2
    exit /b 1
)

echo Compiling with embedded SQLite...
gcc -O2 -Wall -DSQLITE_THREADSAFE=0 -DSQLITE_OMIT_LOAD_EXTENSION -o xojodoc.exe ^
    src\main.c ^
    src\database.c ^
    src\display.c ^
    sqlite3.c ^
    -s

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Build successful! Binary: xojodoc.exe
    echo.
    dir xojodoc.exe | findstr "xojodoc.exe"
    echo.
    echo This is a fully static binary with no dependencies!
    exit /b 0
) else (
    echo.
    echo Build failed!
    exit /b 1
)
