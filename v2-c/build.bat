@echo off
REM Build script for Windows (MinGW/MSVC)

echo Building XojoDoc v2.0 (C Edition)...

REM Check for GCC
where gcc >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo Using GCC compiler...
    
    REM Try with pkg-config first (if available)
    pkg-config --exists sqlite3 >nul 2>nul
    if %ERRORLEVEL% EQU 0 (
        echo Found SQLite3 via pkg-config...
        for /f %%i in ('pkg-config --cflags sqlite3') do set SQLITE_CFLAGS=%%i
        for /f %%i in ('pkg-config --libs sqlite3') do set SQLITE_LIBS=%%i
        
        gcc -O2 -Wall %SQLITE_CFLAGS% -o xojodoc.exe ^
            src\main.c ^
            src\database.c ^
            src\display.c ^
            %SQLITE_LIBS% ^
            -s
    ) else (
        REM Fallback: try common MinGW paths
        echo Trying standard MinGW paths...
        gcc -O2 -Wall -o xojodoc.exe ^
            src\main.c ^
            src\database.c ^
            src\display.c ^
            -lsqlite3 ^
            -s
    )
    
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo Build successful! Binary: xojodoc.exe
        echo.
        dir xojodoc.exe | findstr "xojodoc.exe"
        exit /b 0
    ) else (
        echo.
        echo Build failed with GCC.
        echo.
        echo If SQLite3 is not found, install it:
        echo   pacman -S mingw-w64-x86_64-sqlite3  (MSYS2/MinGW)
        echo.
        echo Or use build-static.bat to build with embedded SQLite
        exit /b 1
    )
)

REM Check for MSVC
where cl >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo Using MSVC compiler...
    cl /O2 /W3 /Fe:xojodoc.exe ^
        src/main.c ^
        src/database.c ^
        src/display.c ^
        sqlite3.lib
    
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo Build successful! Binary: xojodoc.exe
        echo.
        dir xojodoc.exe | findstr "xojodoc.exe"
        exit /b 0
    ) else (
        echo.
        echo Build failed with MSVC.
        exit /b 1
    )
)

echo ERROR: No compiler found!
echo Please install MinGW (gcc) or MSVC.
echo.
echo For MinGW: https://winlibs.com/
echo For MSVC: Install Visual Studio Build Tools
exit /b 1
