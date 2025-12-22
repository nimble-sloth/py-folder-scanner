import os
import pathlib

def write_tree(root: str) -> str:
    root = pathlib.Path(root).resolve()
    lines = ["FULL PROJECT STRUCTURE", f"{root.name}\\"]

    for path in root.rglob("*"):
        rel = path.relative_to(root)
        depth = len(rel.parts) - 1
        indent = "|   " * depth
        prefix = "|-- "
        lines.append(f"{indent}{prefix}{path.name}")

    lines.append("---- END OF TREE ----")
    return "\n".join(lines)
