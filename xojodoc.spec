# -*- mode: python ; coding: utf-8 -*-

"""
PyInstaller spec file for XojoDoc.

Builds a single-file executable for Windows.
"""

import sys
from pathlib import Path

block_cipher = None

# Get paths
project_root = Path.cwd()
src_path = project_root / 'src'

a = Analysis(
    ['src/xojodoc/cli.py'],
    pathex=[str(src_path)],
    binaries=[],
    datas=[
        # Include template file
        ('xojodoc.conf.template', '.'),
    ],
    hiddenimports=[
        'xojodoc.database',
        'xojodoc.parser',
        'xojodoc.indexer',
        'xojodoc.tui',
        'xojodoc.config',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'PIL',
        'tkinter',
    ],
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
    name='xojodoc',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path here if you have one
)
