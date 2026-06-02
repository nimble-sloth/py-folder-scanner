import os
import pathlib


def write_tree(root: str, skip_folders=None) -> str:
    root = pathlib.Path(root).resolve()
    skip = {s.strip().lower() for s in (skip_folders or []) if s.strip()}

    lines = [
        "FULL PROJECT STRUCTURE",
        f"{root.name}\\"
    ]

    def add_directory(path: pathlib.Path, prefix: str = ""):
        try:
            entries = sorted(
                path.iterdir(),
                key=lambda p: (not p.is_dir(), p.name.lower())
            )
        except PermissionError:
            lines.append(f"{prefix}|-- [permission denied]")
            return

        entries = [
            entry for entry in entries
            if not (entry.is_dir() and entry.name.lower() in skip)
        ]

        for entry in entries:
            lines.append(f"{prefix}|-- {entry.name}")

            if entry.is_dir():
                add_directory(entry, prefix + "|   ")

    add_directory(root)

    lines.append("---- END OF TREE ----")
    return "\n".join(lines)