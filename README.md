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

```bash
python -m PyInstaller folder-scanner.spec
```

## This generates the executable here:

```bash
dist/folder-scanner.exe
```

## Pushing Changes to Git (from Terminal)

Use the following commands inside the project folder:

### 1. Check which files changed
```bash
git status
git add .
git commit -m "Your commit message"
git push
git push -u origin main
```