"""Validate the published notebooks without executing their computations."""

from __future__ import annotations

import ast
import json
from pathlib import Path

import nbformat

from refactor_notebooks import NOTEBOOKS, ROOT


def python_source(source: str) -> str:
    """Remove line-oriented IPython commands before parsing Python code."""
    lines = source.splitlines()
    if lines and lines[0].lstrip().startswith("%%"):
        return ""
    return "\n".join(
        "" if line.lstrip().startswith(("%", "!")) else line for line in lines
    )


def validate_published_notebook(path: Path) -> None:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    combined_markdown = "\n".join(
        "".join(cell["source"])
        for cell in notebook["cells"]
        if cell["cell_type"] == "markdown"
    )
    combined_code = "\n".join(
        "".join(cell["source"])
        for cell in notebook["cells"]
        if cell["cell_type"] == "code"
    )

    if "## Fundamentos" not in combined_markdown:
        raise ValueError(f"{path}: missing the conceptual overview")
    if "## Cómo usar la herramienta" not in combined_markdown:
        raise ValueError(f"{path}: missing the usage overview")
    if combined_code.count("# Figure style shared by every chapter") != 1:
        raise ValueError(f"{path}: the shared figure style must occur exactly once")
    if '"figure.constrained_layout.use": False' not in combined_code:
        raise ValueError(f"{path}: incompatible Matplotlib layout configuration")

    for index, cell in enumerate(notebook["cells"]):
        if cell["cell_type"] != "code":
            continue
        for output in cell.get("outputs", []):
            if output.get("output_type") == "error":
                raise ValueError(f"{path}: error output in cell {index}")
        try:
            ast.parse(python_source("".join(cell["source"])))
        except SyntaxError as error:
            raise SyntaxError(f"{path}: invalid Python in cell {index}") from error


def main() -> None:
    # Build artifacts may contain copied notebooks from previous runs; validate
    # authored material only.
    all_notebooks = sorted((ROOT / "notebooks").rglob("*.ipynb"))
    for path in all_notebooks:
        with path.open(encoding="utf-8") as stream:
            nbformat.validate(nbformat.read(stream, as_version=4))

    for relative_path in NOTEBOOKS:
        validate_published_notebook(ROOT / relative_path)

    print(
        f"Validated {len(all_notebooks)} notebooks structurally and "
        f"{len(NOTEBOOKS)} published notebooks editorially."
    )


if __name__ == "__main__":
    main()
