@echo off
REM Build the Hand & Voice Control executable
REM Usage: build\build.bat

echo ============================================
echo  Building Hand ^& Voice Control .exe
echo ============================================

cd /d "%~dp0\.."
call venv\Scripts\activate

echo.
echo Running PyInstaller...
pyinstaller build\build.spec --clean --noconfirm

echo.
if exist "dist\HandVoiceControl.exe" (
    echo BUILD SUCCESSFUL
    echo Output: dist\HandVoiceControl.exe
    echo.
    dir /b dist\HandVoiceControl.exe
) else (
    echo BUILD FAILED — check output above for errors
)

pause
