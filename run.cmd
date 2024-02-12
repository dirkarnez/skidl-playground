@echo off
set PYTHON_DIR=%USERPROFILE%\Downloads\python-3.10.8-amd64-portable
set PATH=%PYTHON_DIR%;%PYTHON_DIR%\Scripts

set KICAD_SYMBOL_DIR=%USERPROFILE%\Downloads\kicad-6.0.11-x86_64\share\kicad\symbols

python main.py

pause
