import os
import pathlib

def scan_tree(root: str, skip_folders, exts):
    root = pathlib.Path(root).resolve()
    out = []

    for path in root.rglob("*"):
        if path.is_dir():
            if path.name.lower() in [s.lower() for s in skip_folders]:
                continue
            continue

        if exts:
            name = path.name.lower()
            if not any(name.endswith(e.lower()) or name == e.lower() for e in exts):
                continue

        try:
            data = path.read_text(errors="ignore")
        except Exception as e:
            out.append(f"[could not read: {e}]")
            continue

        out.append(f"=== File: {path} ===\n{data}\n")

    return "\n".join(out)
