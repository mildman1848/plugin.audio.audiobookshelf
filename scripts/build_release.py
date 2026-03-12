#!/usr/bin/env python3

from __future__ import annotations

import shutil
from pathlib import Path
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
DIST_DIR = ROOT / "dist"


def addon_dir() -> Path:
    matches = sorted(
        path.parent
        for path in ROOT.glob("*/addon.xml")
        if path.parent.name not in {"dist", "node_modules", ".github", "tmp"}
    )
    if len(matches) != 1:
        raise RuntimeError(f"Expected exactly one addon directory, found {len(matches)}: {matches}")
    return matches[0]


def addon_version(addon_root: Path) -> str:
    tree = ElementTree.parse(addon_root / "addon.xml")
    return tree.getroot().attrib["version"]


def build_zip() -> Path:
    addon_root = addon_dir()
    version = addon_version(addon_root)
    DIST_DIR.mkdir(exist_ok=True)
    archive_base = DIST_DIR / f"{addon_root.name}-{version}"
    archive_path = shutil.make_archive(str(archive_base), "zip", ROOT, addon_root.name)
    return Path(archive_path)


def main() -> None:
    archive = build_zip()
    print(archive)


if __name__ == "__main__":
    main()
