@echo off
setlocal
cd /d "%~dp0"

python -m pip install -r requirements.txt -r requirements-build.txt
if errorlevel 1 exit /b %errorlevel%

python -m PyInstaller --noconfirm --clean --onefile --console ^
  --name LessonPlanGenerator ^
  --add-data "templates;templates" ^
  --add-data "static;static" ^
  launcher.py
if errorlevel 1 exit /b %errorlevel%

echo.
echo Build complete: %~dp0dist\LessonPlanGenerator.exe
endlocal
