#!/usr/bin/env python3
"""
Script pentru generarea executabilului AutoConta
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def check_dependencies():
    """Verifică dacă toate dependințele sunt instalate"""
    required_packages = [
        'pyinstaller',
        'pdfplumber',
        'python-docx',
        'docxtpl',
        'pytesseract',
        'opencv-python',
        'pdf2image',
        'Pillow',
        'numpy'
    ]

    missing_packages = []

    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✓ {package} - instalat")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package} - LIPSĂ")

    if missing_packages:
        print(f"\nPachete lipsă: {', '.join(missing_packages)}")
        install = input("Vrei să instalez pachetele lipsă? (y/n): ")
        if install.lower() in ['y', 'yes', 'da']:
            for package in missing_packages:
                subprocess.run([sys.executable, '-m', 'pip', 'install', package])
        else:
            print("Nu pot continua fără toate dependințele.")
            return False

    return True


def create_spec_file():
    """Creează fișierul .spec pentru PyInstaller cu configurație personalizată"""

    spec_content = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Detectează dacă Tesseract este instalat și adaugă căile necesare
import os
import sys
from pathlib import Path

# Caută Tesseract în locațiile obișnuite
tesseract_paths = [
    r"C:\\Program Files\\Tesseract-OCR",
    r"C:\\Program Files (x86)\\Tesseract-OCR",
]

tesseract_data = []
tesseract_path = None

for path in tesseract_paths:
    if os.path.exists(path):
        tesseract_path = path
        # Adaugă fișierele de date Tesseract
        tessdata_path = os.path.join(path, 'tessdata')
        if os.path.exists(tessdata_path):
            tesseract_data.append((tessdata_path, 'tessdata'))
        break

# Date și fișiere suplimentare
added_files = [
    ('IMPUTERNICIRE_model_ro_eng.docx', '.'),  # Template-ul procurii
]

# Adaugă Tesseract data dacă există
added_files.extend(tesseract_data)

# Hidden imports pentru bibliotecile care nu sunt detectate automat
hidden_imports = [
    'pdfplumber',
    'docxtpl',
    'docx',
    'pytesseract', 
    'cv2',
    'pdf2image',
    'PIL',
    'PIL.Image',
    'PIL.ImageTk',
    'numpy',
    'tkinter',
    'tkinter.ttk',
    'tkinter.filedialog',
    'tkinter.messagebox',
    'tkinter.simpledialog',
    'pathlib',
    'tempfile',
    'logging',
    're',
    'os',
    'sys'
]

a = Analysis(
    ['AutoConta.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AutoConta',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Pentru aplicație GUI
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)
"""

    with open('AutoConta.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)

    print("✓ Fișierul AutoConta.spec a fost creat")


def build_executable():
    """Construiește executabilul folosind PyInstaller"""

    print("Construiesc executabilul...")

    # Comandă PyInstaller
    cmd = [
        'pyinstaller',
        '--clean',
        '--noconfirm',
        'AutoConta.spec'
    ]

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✓ Executabilul a fost creat cu succes!")
        print(f"Locația: {os.path.abspath('dist/AutoConta.exe')}")

        # Copiază template-ul în directorul dist dacă nu e deja acolo
        template_src = 'IMPUTERNICIRE_model_ro_eng.docx'
        template_dst = 'dist/IMPUTERNICIRE_model_ro_eng.docx'

        if os.path.exists(template_src) and not os.path.exists(template_dst):
            shutil.copy2(template_src, template_dst)
            print(f"✓ Template copiat în {template_dst}")

    except subprocess.CalledProcessError as e:
        print(f"✗ Eroare la construirea executabilului:")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return False

    return True


def cleanup():
    """Curăță fișierele temporare"""
    cleanup_dirs = ['build', '__pycache__']
    cleanup_files = ['*.pyc']

    for dir_name in cleanup_dirs:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✓ Șters director: {dir_name}")


def create_installer_script():
    """Creează un script pentru instalarea dependințelor externe"""

    installer_content = """@echo off
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
"""

    with open('install_dependencies.bat', 'w', encoding='utf-8') as f:
        f.write(installer_content)

    print("✓ Creat install_dependencies.bat")


def main():
    """Funcția principală"""

    print("=== AutoConta Executable Builder ===\n")

    # Verifică structura proiectului
    required_files = ['AutoConta.py', 'generare_procuri.py']
    template_file = 'IMPUTERNICIRE_model_ro_eng.docx'

    missing_files = [f for f in required_files if not os.path.exists(f)]

    if missing_files:
        print(f"✗ Fișiere lipsă: {', '.join(missing_files)}")
        print("Te rog să rulezi acest script din directorul proiectului.")
        return

    if not os.path.exists(template_file):
        print(f"⚠ Template-ul '{template_file}' nu a fost găsit.")
        print("Aplicația va funcționa, dar va căuta template-ul în timpul rulării.")
    else:
        print(f"✓ Template găsit: {template_file}")

    print("\n1. Verificarea dependințelor...")
    if not check_dependencies():
        return

    print("\n2. Crearea fișierului .spec...")
    create_spec_file()

    print("\n3. Construirea executabilului...")
    if not build_executable():
        return

    print("\n4. Curățarea fișierelor temporare...")
    cleanup()

    print("\n5. Crearea script-ului de instalare...")
    create_installer_script()

    print("\n=== Build Finalizat ===")
    print("\nExecutabilul se află în: dist/AutoConta.exe")
    print("\nPentru distribuție, copiază:")
    print("- dist/AutoConta.exe")
    print("- dist/IMPUTERNICIRE_model_ro_eng.docx (dacă există)")
    print("\nNotă: Pe sistemele țintă va fi nevoie de:")
    print("- Tesseract OCR instalat")
    print("- Microsoft Visual C++ Redistributable")


if __name__ == "__main__":
    main()