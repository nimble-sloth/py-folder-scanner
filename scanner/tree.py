import os
import pathlib


def write_tree(root: str, skip_folders=None) -> str:
    root = pathlib.Path(root).resolve()
    skip = {s.strip().lower() for s in (skip_folders or []) if s.strip()}

    lines = ["FULL PROJECT STRUCTURE", f"{root.name}\\"]

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d for d in sorted(dirnames)
            if d.lower() not in skip
        ]

        for dirname in dirnames:
            path = pathlib.Path(dirpath) / dirname
            rel = path.relative_to(root)
            depth = len(rel.parts) - 1
            indent = "|   " * depth
            lines.append(f"{indent}|-- {dirname}")

        for filename in sorted(filenames):
            path = pathlib.Path(dirpath) / filename
            rel = path.relative_to(root)
            depth = len(rel.parts) - 1
            indent = "|   " * depth
            lines.append(f"{indent}|-- {filename}")

    lines.append("---- END OF TREE ----")
    return "\n".join(lines)