# py-folder-scanner

A Python-based folder scanner with a modern Qt6 GUI.  
It can:

- Scan a directory tree
- Optionally include a full folder structure dump
- Filter files by extension
- Skip specific folders
- Save results to a chosen output file
- Provide a responsive UI with progress indicator

Built with **PySide6** and structured for maintainability.

## Running

```bash
pip install -r requirements.txt
python main.py

---

## Building the Windows EXE

**PowerShell:**

```powershell
python -m PyInstaller folder-scanner.spec
```

This generates the executable here:

```
dist/folder-scanner/folder-scanner.exe
```