# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['PeppSnipp.py'],
             pathex=['/Users/thewilliams/Code/peppsnipp'],
             binaries=[('/Users/thewilliams/Code/peppsnipp/peppcrawler/driver/ChromeDriver', './peppcrawler/driver')],
             datas=[('/Users/thewilliams/Code/peppsnipp/output', './output')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='PeppSnipp',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
app = BUNDLE(exe,
             name='PeppSnipp.app',
             icon='icon.icns',
             bundle_identifier=None)
