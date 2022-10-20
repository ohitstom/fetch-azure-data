nuitka --onefile --include-plugin-directory=modules --lto=no main.py
rmdir /s main.build
rmdir /s main.dist
rmdir /s main.onefile-build
mkdir build
move main.exe build