#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
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


def addon_root() -> ElementTree.Element:
    return ElementTree.parse(addon_dir() / "addon.xml").getroot()


def read_addon_id() -> str:
    return addon_root().attrib["id"]


def read_version() -> str:
    return addon_root().attrib["version"]


def read_name() -> str:
    return addon_root().attrib["name"]


def read_description() -> str:
    root = addon_root()
    metadata = root.find("./extension[@point='xbmc.addon.metadata']")
    if metadata is None:
        return read_name()
    for tag in ("description", "summary"):
        nodes = metadata.findall(tag)
        for preferred_lang in ("en_GB", "de_DE", None):
            for node in nodes:
                if preferred_lang is None or node.attrib.get("lang") == preferred_lang:
                    text = (node.text or "").strip()
                    if text:
                        return text
    return read_name()


def read_asset_paths() -> list[Path]:
    root = addon_root()
    metadata = root.find("./extension[@point='xbmc.addon.metadata']")
    if metadata is None:
        return []

    assets = metadata.find("assets")
    if assets is None:
        return []

    addon_root_dir = addon_dir()
    paths = []
    seen = set()
    for node in list(assets):
        value = (node.text or "").strip()
        if not value:
            continue
        rel = Path(value)
        if rel in seen:
            continue
        asset_path = addon_root_dir / rel
        if asset_path.is_file():
            paths.append(rel)
            seen.add(rel)
    return paths


def build_zip(version: str) -> Path:
    addon_root_dir = addon_dir()
    DIST_DIR.mkdir(exist_ok=True)
    archive_base = DIST_DIR / f"{addon_root_dir.name}-{version}"
    archive_path = shutil.make_archive(str(archive_base), "zip", ROOT, addon_root_dir.name)
    return Path(archive_path)


def write_index(target_dir: Path, version: str) -> None:
    addon_id = read_addon_id()
    addon_name = read_name()
    addon_description = read_description()
    html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{addon_id}</title>
  </head>
  <body>
    <h1>{addon_name}</h1>
    <p>{addon_description}</p>
    <ul>
      <li><a href="addon.xml">addon.xml</a></li>
      <li><a href="{addon_id}-{version}.zip">{addon_id}-{version}.zip</a></li>
    </ul>
  </body>
</html>
"""
    (target_dir / "index.html").write_text(html, encoding="utf-8")


def update_addons_xml(repo_root: Path) -> None:
    addon_files = sorted(repo_root.glob("repo/*/addon.xml"))
    addon_map = {}
    for addon_file in addon_files:
        root = ElementTree.parse(addon_file).getroot()
        addon_map[root.attrib["id"]] = root

    ordered_ids = []
    current_root = None
    try:
        git_xml = subprocess.run(
            ["git", "show", "HEAD:repo/addons.xml"],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        current_root = ElementTree.fromstring(git_xml)
    except (subprocess.CalledProcessError, FileNotFoundError, ElementTree.ParseError):
        existing_addons_xml = repo_root / "repo" / "addons.xml"
        if existing_addons_xml.exists():
            current_root = ElementTree.parse(existing_addons_xml).getroot()

    if current_root is not None:
        for addon in current_root.findall("addon"):
            addon_id = addon.attrib.get("id")
            if addon_id in addon_map and addon_id not in ordered_ids:
                ordered_ids.append(addon_id)

    for addon_id in sorted(addon_map):
        if addon_id not in ordered_ids:
            ordered_ids.append(addon_id)

    addons = ElementTree.Element("addons")
    for addon_id in ordered_ids:
        addons.append(addon_map[addon_id])

    ElementTree.indent(addons, space="  ")

    xml_body = ElementTree.tostring(addons, encoding="unicode")
    xml_text = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n" + xml_body + "\n"
    addons_xml = repo_root / "repo" / "addons.xml"
    addons_xml.write_text(xml_text, encoding="utf-8")
    md5 = hashlib.md5(xml_text.encode("utf-8")).hexdigest()
    (repo_root / "repo" / "addons.xml.md5").write_text(md5, encoding="utf-8")


def publish(publish_repo: Path) -> Path:
    version = read_version()
    addon_id = read_addon_id()
    addon_root_dir = addon_dir()
    archive = build_zip(version)
    target_dir = publish_repo / "repo" / addon_id
    if target_dir.exists():
        shutil.rmtree(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(addon_root_dir / "addon.xml", target_dir / "addon.xml")
    for rel_path in read_asset_paths():
        destination = target_dir / rel_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(addon_root_dir / rel_path, destination)
    shutil.copy2(archive, target_dir / archive.name)
    write_index(target_dir, version)
    update_addons_xml(publish_repo)
    return target_dir / archive.name


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--publish-repo", required=True, type=Path)
    args = parser.parse_args()
    archive = publish(args.publish_repo.resolve())
    print(archive)


if __name__ == "__main__":
    main()
