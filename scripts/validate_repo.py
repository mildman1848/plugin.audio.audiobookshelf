#!/usr/bin/env python3

from __future__ import annotations

import py_compile
from pathlib import Path
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRS = {".git", "node_modules", "dist", "__pycache__"}


def iter_files(suffix: str):
    for path in ROOT.rglob(f"*{suffix}"):
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        if path.is_file():
            yield path


def validate_python() -> None:
    files = list(iter_files(".py"))
    if not files:
        print("No Python files to validate")
        return
    for path in files:
        py_compile.compile(str(path), doraise=True)
    print(f"Validated Python syntax for {len(files)} files")


def validate_xml() -> None:
    files = list(iter_files(".xml"))
    if not files:
        print("No XML files to validate")
        return
    for path in files:
        ElementTree.parse(path)
    print(f"Validated XML syntax for {len(files)} files")


def main() -> None:
    validate_python()
    validate_xml()


if __name__ == "__main__":
    main()
