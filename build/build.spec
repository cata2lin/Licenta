# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec for Hand & Voice PC Control.

Build command:
    pyinstaller build/build.spec

Output:
    dist/HandVoiceControl.exe
"""

import os
import sys
from pathlib import Path

block_cipher = None

# Resolve project root
ROOT = Path(SPECPATH).parent


# ---------------------------------------------------------------------------
# MediaPipe: bundle the full package tree (includes .tflite and .binarypb)
# ---------------------------------------------------------------------------
def get_mediapipe_path():
    import mediapipe
    return mediapipe.__path__[0]


mediapipe_tree = Tree(
    get_mediapipe_path(),
    prefix='mediapipe',
    excludes=["*.pyc"],
)

a = Analysis(
    [str(ROOT / 'main.py')],
    pathex=[str(ROOT)],
    binaries=[],
    datas=[
        (str(ROOT / 'assets'), 'assets'),
        (str(ROOT / 'settings.json'), '.'),
    ],
    hiddenimports=[
        # MediaPipe + dependencies
        'mediapipe',
        'mediapipe.tasks',
        'mediapipe.tasks.python',
        'mediapipe.tasks.python.vision',
        # Audio
        'sounddevice',
        'webrtcvad',
        # ASR (CTranslate2 backend)
        'faster_whisper',
        'ctranslate2',
        'huggingface_hub',
        'tokenizers',
        # System tray
        'pystray',
        'PIL',
        'PIL.Image',
        'PIL.ImageDraw',
        # Vision
        'cv2',
        'numpy',
        # Win32
        'win32gui',
        'win32con',
        'win32process',
        'ctypes',
        'ctypes.wintypes',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'pandas', 'scipy', 'IPython', 'notebook',
              'PyQt5', 'tkinter', 'unittest', 'tensorboard', 'pytest'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Merge MediaPipe tree into datas
a.datas += mediapipe_tree

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='HandVoiceControl',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon=str(ROOT / 'assets' / 'icon.ico'),  # Uncomment when icon.ico is available
)
