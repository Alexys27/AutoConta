# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Detectează dacă Tesseract este instalat și adaugă căile necesare
import os
import sys
from pathlib import Path

# Caută Tesseract în locațiile obișnuite
tesseract_paths = [
    r"C:\Program Files\Tesseract-OCR",
    r"C:\Program Files (x86)\Tesseract-OCR",
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
