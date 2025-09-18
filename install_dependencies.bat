@echo off
echo Installing AutoConta Dependencies...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python nu este instalat sau nu este in PATH!
    echo Te rog instaleaza Python de la https://python.org
    pause
    exit /b 1
)

REM Install required Python packages
echo Installing Python packages...
pip install pdfplumber python-docx docxtpl pytesseract opencv-python pdf2image Pillow numpy pyinstaller

REM Check if Tesseract is installed
tesseract --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo IMPORTANT: Tesseract OCR nu este instalat!
    echo Te rog descarca si instaleaza Tesseract de la:
    echo https://github.com/UB-Mannheim/tesseract/wiki
    echo.
    echo Asigura-te ca instalezi si language packs pentru romana si engleza.
    echo.
    pause
)

echo.
echo Setup complet! Acum poti rula build_executable.py
pause
