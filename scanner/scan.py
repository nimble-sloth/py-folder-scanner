import os
import pathlib


def _matches_file_filter(path: pathlib.Path, filters):
    if not filters:
        return True

    name = path.name.lower()
    suffix = path.suffix.lower()

    normalized = []
    for item in filters:
        item = item.strip().lower()
        if item:
            normalized.append(item)

    return any(
        name == item or suffix == item or name.endswith(item)
        for item in normalized
    )


def _read_file(path: pathlib.Path):
    try:
        data = path.read_text(encoding="utf-8", errors="replace")
        return f"=== File: {path} ===\n{data}\n"
    except Exception as e:
        return f"=== File: {path} ===\n[could not read: {e}]\n"


def scan_tree(root: str, skip_folders, exts, include_paths=None, root_files=None):
    root = pathlib.Path(root).resolve()
    skip = {s.strip().lower() for s in skip_folders if s.strip()}
    out = []

    include_paths = [p.strip() for p in (include_paths or []) if p.strip()]
    root_files = {f.strip().lower() for f in (root_files or []) if f.strip()}

    # First: scan selected folders only, for example Angular src/
    folders_to_scan = include_paths if include_paths else ["."]

    for include_path in folders_to_scan:
        scan_root = root / include_path
        if not scan_root.exists() or not scan_root.is_dir():
            continue

        for dirpath, dirnames, filenames in os.walk(scan_root):
            dirnames[:] = [
                d for d in dirnames
                if d.lower() not in skip
            ]

            for filename in filenames:
                path = pathlib.Path(dirpath) / filename

                if not _matches_file_filter(path, exts):
                    continue

                out.append(_read_file(path))

    # Second: include critical files from the project root.
    for filename in sorted(root_files):
        path = root / filename
        if path.exists() and path.is_file():
            out.append(_read_file(path))

    return "\n".join(out)
