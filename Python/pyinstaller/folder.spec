# -*- mode: python ; coding: utf-8 -*-

import PyInstaller.config
PyInstaller.config.CONF['distpath'] = '../builds'

block_cipher = None

a = Analysis(['../DesktopApp/main.py'],
             pathex=[],
             binaries=[],
             datas=[('../../miscellaneous/config.ini', '.'),
                    ('../../miscellaneous/columns_info.json', '.'),
                    ('../../miscellaneous/icon.jpg', '.'),
                    ('../../miscellaneous/image_labels.csv', '.')],
             hiddenimports=['sklearn.utils._cython_blas'],
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
          [],
          exclude_binaries=True,
          name='CXR_Classify',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               name='dist_folder',
               strip=False,
               upx=True,
               upx_exclude=[])
