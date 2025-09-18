@echo off
echo ===== AutoConta Quick Build =====

REM Verifică dacă Python este instalat
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python nu este instalat sau nu este in PATH!
    echo Instaleaza Python de la https://python.org
    pause
    exit /b 1
)

echo Installing dependencies...
pip install -r requirements.txt

echo Building executable...
python build_executable.py

echo.
echo Build complet! Verifica directorul 'dist' pentru executabil.
pause