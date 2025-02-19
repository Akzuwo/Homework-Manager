# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Homework-Manager-v1.5.2-dev.pyw'],
    pathex=[],
    binaries=[('C:\\Users\\timow\\AppData\\Local\\Programs\\Python\\Python312\\tcl\\tcl8.6', './tcl/tcl8.6'), ('C:\\Users\\timow\\AppData\\Local\\Programs\\Python\\Python312\\tcl\\tk8.6', './tcl/tk8.6')],
    datas=[('C:\\Users\\timow\\OneDrive\\Documents\\Python Files\\homework_2941554.ico', '.')],
    hiddenimports=['tkcalendar', 'tkcalendar.widgets', 'babel.numbers'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Homework-Manager-v1.5.2-dev',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\timow\\OneDrive\\Documents\\Python Files\\homework_2941554.ico'],
)
