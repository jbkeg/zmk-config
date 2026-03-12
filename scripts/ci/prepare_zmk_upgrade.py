#!/usr/bin/env python3
"""Update local ZMK version pins for a new stable release tag."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--tag",
        required=True,
        help="Stable ZMK release tag to pin, for example v0.3.0.",
    )
    return parser.parse_args()


def split_version(tag: str) -> tuple[str, str]:
    match = re.fullmatch(r"v(\d+)\.(\d+)\.(\d+)", tag.strip())
    if not match:
        raise ValueError(f"Expected stable tag like v0.3.0, got '{tag}'.")
    major, minor, _patch = match.groups()
    return tag.strip(), f"v{major}.{minor}"


def write_if_changed(path: Path, content: str) -> bool:
    previous = path.read_text(encoding="utf-8")
    if previous == content:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def update_version_file(path: Path, tag: str) -> bool:
    return write_if_changed(path, f"{tag}\n")


def update_tests_west(path: Path, tag: str) -> bool:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    found_revision = False

    in_zmk_project = False
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped == "- name: zmk":
            in_zmk_project = True
            continue

        if in_zmk_project and re.fullmatch(r"\s*revision:\s*v\d+\.\d+\.\d+\s*", stripped):
            indent = re.match(r"\s*", line).group(0)
            newline = "\n" if line.endswith("\n") else ""
            lines[index] = f"{indent}revision: {tag}{newline}"
            found_revision = True
            break

    if not found_revision:
        raise ValueError(f"Could not find the zmk project revision in {path}.")

    return write_if_changed(path, "".join(lines))


def update_config_defaults(path: Path, minor_tag: str) -> bool:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    found_defaults_revision = False

    in_defaults = False
    defaults_indent = 0
    for index, line in enumerate(lines):
        stripped = line.strip()
        indent = len(line) - len(line.lstrip(" "))

        if stripped == "defaults:":
            in_defaults = True
            defaults_indent = indent
            continue

        if not in_defaults:
            continue

        if stripped.startswith("#") or stripped == "":
            continue

        if indent <= defaults_indent:
            in_defaults = False
            continue

        if re.fullmatch(r"\s*revision:\s*v\d+\.\d+\s*", stripped):
            line_indent = re.match(r"\s*", line).group(0)
            newline = "\n" if line.endswith("\n") else ""
            lines[index] = f"{line_indent}revision: {minor_tag}{newline}"
            found_defaults_revision = True
            break

    if not found_defaults_revision:
        raise ValueError(f"Could not find manifest.defaults.revision in {path}.")

    return write_if_changed(path, "".join(lines))


def update_build_profiles(path: Path, minor_tag: str) -> bool:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    in_stable = False
    stable_indent = 0
    found_revision = False
    found_cache_key = False

    for index, line in enumerate(lines):
        stripped = line.strip()
        indent = len(line) - len(line.lstrip(" "))

        if stripped == '"stable": {':
            in_stable = True
            stable_indent = indent
            continue

        if not in_stable:
            continue

        if indent == stable_indent and stripped == "},":
            in_stable = False
            continue

        if '"zmk_revision":' in line:
            match = re.search(r'("zmk_revision":\s*")v\d+\.\d+(")', line)
            if not match:
                raise ValueError(f"Could not update stable zmk_revision in {path}.")
            lines[index] = f"{line[:match.start(0)]}{match.group(1)}{minor_tag}{match.group(2)}{line[match.end(0) :]}"
            found_revision = True
            continue

        if '"cache_key":' in line:
            match = re.search(r'(stable-[^"]*-?)v\d+\.\d+(")', line)
            if not match:
                raise ValueError(f"Could not update stable cache_key in {path}.")
            lines[index] = f"{line[:match.start(0)]}{match.group(1)}{minor_tag}{match.group(2)}{line[match.end(0) :]}"
            found_cache_key = True

    if not found_revision:
        raise ValueError(f"Could not find the stable zmk_revision entry in {path}.")
    if not found_cache_key:
        raise ValueError(f"Could not find the stable cache_key entry in {path}.")

    return write_if_changed(path, "".join(lines))


def main() -> int:
    args = parse_args()
    full_tag, minor_tag = split_version(args.tag)

    changed_files: list[str] = []

    if update_version_file(REPO_ROOT / "VERSION", full_tag):
        changed_files.append("VERSION")
    if update_config_defaults(REPO_ROOT / "config" / "west.yml", minor_tag):
        changed_files.append("config/west.yml")
    if update_tests_west(REPO_ROOT / "tests" / "west.yml", full_tag):
        changed_files.append("tests/west.yml")
    if update_build_profiles(REPO_ROOT / "scripts" / "build_profiles.py", minor_tag):
        changed_files.append("scripts/build_profiles.py")

    if changed_files:
        print("Updated:")
        for changed_path in changed_files:
            print(f"- {changed_path}")
    else:
        print("No version pin changes were needed.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
