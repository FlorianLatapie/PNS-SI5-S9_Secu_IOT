@echo off
setlocal enabledelayedexpansion

REM List of required DLL files
set "requiredFiles=globalplatform.dll gppcscconnectionplugin.dll gpshell.exe legacy.dll libcrypto-1_1.dll libcrypto-3.dll libssl-1_1.dll libssl-3.dll vcruntime140.dll zlibwapi.dll"

REM Check if all required files are present
set "missingFiles="
for %%F in (%requiredFiles%) do (
    if not exist "%%F" (
        set "missingFiles=!missingFiles! %%F"
    )
)

if not "%missingFiles%"=="" (
    echo The following files are missing:%missingFiles%, please download them from https://kaoh.github.io/globalplatform/
    exit /b 1
) else (
    echo All required files of gpshell are present.
    exit /b 0
)

endlocal
