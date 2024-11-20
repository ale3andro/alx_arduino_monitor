# -*- mode: python -*-

# https://stackoverflow.com/questions/63585632/how-to-add-a-truetype-font-file-to-a-pyinstaller-executable-for-use-with-pygame

block_cipher = None


a = Analysis(['test_001.py'],
             pathex=['C:\\Users\\ale3a\\alx_arduino_logger', 'C:\\Users\\ale3a\\alx_arduino_logger\\env\\Lib\\site-packages'], 
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

a.datas += [('ttf file','font\\Ubuntu.ttf', "DATA")]

pyz = PYZ(a.pure, a.zipped_data,
         cipher=block_cipher)

exe = EXE(pyz,
      a.scripts,
      a.binaries,
      a.zipfiles,
      a.datas,
      name="ale3andro's Arduino Monitor",
      debug=False,
      strip=False,
      upx=True,
      console=False # set True if command prompt window needed
)