# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:/Users/Space/ChatAssistant/main.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Users/Space/ChatAssistant/games', 'games/'), ('C:/Users/Space/ChatAssistant/modules', 'modules/')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ChatAssistant v1.1',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\Space\\ChatAssistant\\imgs\\assist_icon.png'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ChatAssistant v1.1',
)
