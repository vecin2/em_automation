# -*- mode: python -*-

block_cipher = None


a = Analysis(['clip.py'],
             pathex=['C:\\dev\\python\\em_automation'],
             binaries=[],
             datas=[],
             hiddenimports=['sql_gen.sqltask_jinja.filters.default','sql_gen.sqltask_jinja.filters.codepath', 'sql_gen.sqltask_jinja.filters.description','sql_gen.sqltask_jinja.filters.suggest'],
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
          name='sqltask',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
