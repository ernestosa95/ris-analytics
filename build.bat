@echo off
setlocal
rem ==========================================================
rem  Compila RIS Analytics: ejecutable (PyInstaller) + instalador (Inno Setup)
rem  Uso: doble clic o "build.bat" desde la carpeta del proyecto
rem ==========================================================

cd /d "%~dp0"

echo.
echo [1/3] Buscando Inno Setup...
set "ISCC="
where ISCC >nul 2>nul && set "ISCC=ISCC"
if not defined ISCC if exist "%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe" set "ISCC=%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe"
if not defined ISCC if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" set "ISCC=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
if not defined ISCC if exist "%ProgramFiles%\Inno Setup 6\ISCC.exe" set "ISCC=%ProgramFiles%\Inno Setup 6\ISCC.exe"
if not defined ISCC (
    echo ERROR: No se encontro Inno Setup ^(ISCC.exe^).
    echo Instalalo con: winget install JRSoftware.InnoSetup
    goto :error
)
echo   OK: %ISCC%

echo.
echo [2/3] Compilando ejecutable con PyInstaller...
pyinstaller --noconfirm --clean RIS_Analytics.spec
if errorlevel 1 (
    echo ERROR: Fallo PyInstaller.
    goto :error
)
if not exist "dist\RIS_Analytics.exe" (
    echo ERROR: No se genero dist\RIS_Analytics.exe
    goto :error
)

echo.
echo [3/3] Generando instalador con Inno Setup...
"%ISCC%" installer.iss
if errorlevel 1 (
    echo ERROR: Fallo Inno Setup.
    goto :error
)

echo.
echo ==========================================================
echo  Compilacion exitosa. Instalador generado en:
dir /b "Output\Instalador_RIS_Analytics_*.exe"
echo ==========================================================
pause
exit /b 0

:error
echo.
echo  La compilacion NO se completo.
pause
exit /b 1
