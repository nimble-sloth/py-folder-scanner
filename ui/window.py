import os
import time
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit,
    QFileDialog, QGridLayout, QCheckBox, QHBoxLayout, QProgressBar, QScrollArea
)
from PySide6.QtCore import Qt, QThread, Signal

from scanner.tree import write_tree
from scanner.scan import scan_tree


class ScanWorker(QThread):
    finished = Signal(str, float, str)  # status, seconds, error

    def __init__(self, folder, output, skip, exts, include_tree):
        super().__init__()
        self.folder = folder
        self.output = output
        self.skip = skip
        self.exts = exts
        self.include_tree = include_tree

    def run(self):
        start = time.time()
        try:
            with open(self.output, "w", encoding="utf-8") as f:
                if self.include_tree:
                    f.write(write_tree(self.folder))
                    f.write("\n\n")

                f.write(scan_tree(self.folder, self.skip, self.exts))

            self.finished.emit("Done", time.time() - start, "")
        except Exception as e:
            self.finished.emit("Error", 0, str(e))


class FolderScannerApp:
    def __init__(self):
        self.app = QApplication([])
        self.window = QWidget()
        self.window.setWindowTitle("Smart Folder Scanner (Python Edition)")
        self.window.resize(800, 700)

        layout = QVBoxLayout(self.window)

        # Header
        layout.addWidget(QLabel("<h2>Smart Folder Scanner</h2>"))

        # Get user directory
        user_dir = os.path.expanduser("~")
        default_scan_dir = user_dir
        default_output_file = os.path.join(user_dir, "Downloads", "scanned_files_output.txt")

        # Folder picker
        self.folder_entry = QLineEdit(default_scan_dir)
        btn_folder = QPushButton("Browse…")
        btn_folder.clicked.connect(self.pick_folder)

        row = QHBoxLayout()
        row.addWidget(self.folder_entry)
        row.addWidget(btn_folder)
        layout.addWidget(QLabel("Folder to scan:"))
        layout.addLayout(row)

        # Output file picker
        self.output_entry = QLineEdit(default_output_file)
        btn_output = QPushButton("Save As…")
        btn_output.clicked.connect(self.pick_output)

        row2 = QHBoxLayout()
        row2.addWidget(self.output_entry)
        row2.addWidget(btn_output)
        layout.addWidget(QLabel("Output file:"))
        layout.addLayout(row2)

        # Skip folders
        self.skip_entry = QLineEdit(".git,node_modules,dist,build,.idea,.vscode")
        layout.addWidget(QLabel("Folders to skip (comma-separated):"))
        layout.addWidget(self.skip_entry)

        # Extensions grid
        ext_defaults = [
            ".go", ".py", ".java", ".js", ".ts", ".tsx", ".jsx",
            ".html", ".css", ".json", ".md",
            ".yaml", ".yml", ".xml",
            ".sh", ".bat", ".ps1", ".sql",
            ".cs", ".cpp", ".c", ".h",
            ".kt", ".rs", ".swift", ".php", ".rb", ".properties",
        ]

        layout.addWidget(QLabel("File types to include:"))

        grid = QGridLayout()
        self.ext_checks = {}

        for i, ext in enumerate(ext_defaults):
            c = QCheckBox(ext)
            if ext in [".go", ".py", ".java"]:
                c.setChecked(True)
            self.ext_checks[ext] = c
            grid.addWidget(c, i // 5, i % 5)

        layout.addLayout(grid)

        # Custom extensions
        self.custom_ext = QLineEdit()
        self.custom_ext.setPlaceholderText(".toml,.gradle,README,LICENSE")
        layout.addWidget(QLabel("Custom extensions or filenames:"))
        layout.addWidget(self.custom_ext)

        # Include tree
        self.include_tree = QCheckBox("Include folder tree")
        self.include_tree.setChecked(True)
        layout.addWidget(self.include_tree)

        # Status + progress
        self.status = QLabel("Ready.")
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.hide()

        layout.addWidget(self.status)
        layout.addWidget(self.progress)

        # Scan button
        self.btn_scan = QPushButton("Scan")
        self.btn_scan.clicked.connect(self.start_scan)
        layout.addWidget(self.btn_scan)

    def pick_folder(self):
        # Start with current value in the text field
        current_path = self.folder_entry.text().strip()
        if not current_path or not os.path.exists(current_path):
            current_path = os.path.expanduser("~")
        
        path = QFileDialog.getExistingDirectory(
            self.window, 
            "Select Folder",
            current_path  # Start dialog at current path
        )
        if path:
            self.folder_entry.setText(path)

    def pick_output(self):
        # Start with current value in the text field
        current_path = self.output_entry.text().strip()
        if not current_path:
            current_path = os.path.join(os.path.expanduser("~"), "Downloads")
        
        # Get directory from current path
        current_dir = os.path.dirname(current_path) if os.path.dirname(current_path) else current_path
        
        path, _ = QFileDialog.getSaveFileName(
            self.window, 
            "Save Output", 
            current_path if os.path.isdir(current_path) or not os.path.exists(current_dir) else current_path,
            "Text Files (*.txt)"
        )
        if path:
            self.output_entry.setText(path)

    def start_scan(self):
        folder = self.folder_entry.text().strip()
        output = self.output_entry.text().strip()

        if not folder or not output:
            self.status.setText("Missing folder or output file")
            return

        skip = [s.strip() for s in self.skip_entry.text().split(",") if s.strip()]
        exts = [e for e, c in self.ext_checks.items() if c.isChecked()]

        if self.custom_ext.text().strip():
            exts += [s.strip() for s in self.custom_ext.text().split(",")]

        self.progress.show()
        self.status.setText("Scanning…")
        self.btn_scan.setEnabled(False)

        self.worker = ScanWorker(folder, output, skip, exts, self.include_tree.isChecked())
        self.worker.finished.connect(self.scan_done)
        self.worker.start()

    def scan_done(self, status, seconds, error):
        self.progress.hide()
        self.btn_scan.setEnabled(True)

        if error:
            self.status.setText(f"Error: {error}")
        else:
            self.status.setText(f"{status} in {seconds:.1f}s")

    def run(self):
        self.window.show()
        self.app.exec()