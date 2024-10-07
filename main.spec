# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['cookiecutter', 'arrow', 'markdown_it_py', 'mdurl', 'oauthlib', 'pypng', 'qrcode', 'rich', 'Pygments', 'watchdog', 'watchfiles', 'requests', 'urllib3', 'certifi', 'charset_normalizer', 'idna', 'fastapi', 'starlette', 'uvicorn', 'h11', 'httptools', 'websockets'],
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
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
