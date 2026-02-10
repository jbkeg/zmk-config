#!/usr/bin/env python3
"""Local Docker runner that mirrors ZMK build-user-config workflow behavior."""

from __future__ import annotations

import argparse
import fnmatch
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str], cwd: Path | None = None) -> None:
    print("+", " ".join(shlex.quote(part) for part in cmd), flush=True)
    subprocess.run(cmd, cwd=str(cwd) if cwd else None, check=True)


def load_matrix(build_matrix_path: Path) -> list[dict[str, Any]]:
    data = yaml.safe_load(build_matrix_path.read_text(encoding="utf-8")) or {}
    include = data.get("include", [])
    if not isinstance(include, list):
        raise ValueError(f"`include` must be a list in {build_matrix_path}")
    return [entry for entry in include if isinstance(entry, dict)]


def default_artifact_name(entry: dict[str, Any]) -> str:
    shield = str(entry.get("shield", "")).strip()
    board = str(entry.get("board", "")).strip().replace("/", "_")
    if shield:
        return f"{shield.replace(' ', '-')}-{board}-zmk"
    return f"{board}-zmk"


def artifact_name(entry: dict[str, Any]) -> str:
    name = str(entry.get("artifact-name", "")).strip()
    return name if name else default_artifact_name(entry)


def filter_matrix(entries: list[dict[str, Any]], patterns: list[str]) -> list[dict[str, Any]]:
    if not patterns:
        return entries

    names = [artifact_name(entry) for entry in entries]
    unmatched_patterns = [
        pattern for pattern in patterns if not any(fnmatch.fnmatchcase(name, pattern) for name in names)
    ]
    if unmatched_patterns:
        raise ValueError(
            "artifact-name pattern(s) matched nothing: "
            + ", ".join(unmatched_patterns)
            + ". Use --list to see valid names."
        )

    selected_entries = [
        entry
        for entry in entries
        if any(fnmatch.fnmatchcase(artifact_name(entry), pattern) for pattern in patterns)
    ]
    return selected_entries


def ensure_config_copy(src_config: Path, dst_base: Path, config_name: str) -> Path:
    dst_config = dst_base / config_name
    if dst_config.exists():
        shutil.rmtree(dst_config)
    dst_config.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src_config, dst_config)
    return dst_config


def stage_extra_modules_from_git(repo_root: Path, dst_base: Path) -> Path:
    """Stage module files from git-visible paths, excluding ignored workspace noise."""
    staged_root = dst_base / "_extra_modules" / "workspace-module"
    if staged_root.exists():
        shutil.rmtree(staged_root)
    staged_root.mkdir(parents=True, exist_ok=True)

    try:
        listed = subprocess.run(
            ["git", "ls-files", "-co", "--exclude-standard", "-z"],
            cwd=str(repo_root),
            check=True,
            capture_output=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return repo_root

    rel_paths = [p for p in listed.stdout.decode("utf-8", errors="surrogateescape").split("\0") if p]
    if not rel_paths:
        return repo_root

    for rel in rel_paths:
        src = repo_root / rel
        if not src.exists() or src.is_dir():
            continue
        dst = staged_root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    return staged_root


def override_zmk_revision(config_dir: Path, revision: str) -> None:
    west_manifest = config_dir / "west.yml"
    if not west_manifest.exists():
        raise FileNotFoundError(f"Cannot override ZMK revision, missing: {west_manifest}")

    data = yaml.safe_load(west_manifest.read_text(encoding="utf-8")) or {}
    manifest = data.get("manifest")
    if not isinstance(manifest, dict):
        raise ValueError(f"Invalid west manifest format: {west_manifest}")

    projects = manifest.get("projects")
    if not isinstance(projects, list):
        raise ValueError(f"Invalid west projects list: {west_manifest}")

    updated = False
    for project in projects:
        if isinstance(project, dict) and project.get("name") == "zmk":
            project["revision"] = revision
            updated = True
            break

    if not updated:
        raise ValueError(f"No 'zmk' project entry found in {west_manifest}")

    west_manifest.write_text(
        yaml.safe_dump(data, sort_keys=False, default_flow_style=False),
        encoding="utf-8",
    )


def remove_stale_git_locks(base_dir: Path) -> list[Path]:
    removed: list[Path] = []

    for git_dir in base_dir.rglob(".git"):
        if not git_dir.is_dir():
            continue
        for lock_file in git_dir.rglob("*.lock"):
            if not lock_file.is_file():
                continue
            lock_file.unlink(missing_ok=True)
            removed.append(lock_file)

    return removed


def ensure_west_ready(base_dir: Path, config_dir: Path, skip_update: bool) -> None:
    if not (base_dir / ".west").exists():
        run(["west", "init", "-l", str(config_dir)], cwd=base_dir)
    else:
        run(["west", "config", "manifest.path", config_dir.name], cwd=base_dir)

    if not skip_update:
        try:
            run(["west", "update", "--fetch-opt=--filter=tree:0"], cwd=base_dir)
        except subprocess.CalledProcessError:
            removed = remove_stale_git_locks(base_dir)
            if not removed:
                raise
            print(
                f"Detected stale git lock files. Removed {len(removed)} lock file(s) and retrying west update.",
                flush=True,
            )
            run(["west", "update", "--fetch-opt=--filter=tree:0"], cwd=base_dir)
    run(["west", "zephyr-export"], cwd=base_dir)


def build_entry(
    *,
    entry: dict[str, Any],
    base_dir: Path,
    build_root: Path,
    output_dir: Path,
    config_dir: Path,
    fallback_binary: str,
    extra_modules_dir: Path | None,
) -> Path:
    board = str(entry.get("board", "")).strip()
    if not board:
        raise ValueError(f"Missing board in matrix entry: {entry}")

    shield = str(entry.get("shield", "")).strip()
    snippet = str(entry.get("snippet", "")).strip()
    cmake_args = str(entry.get("cmake-args", "")).strip()

    artifact = artifact_name(entry)
    build_dir = build_root / artifact
    build_root.mkdir(parents=True, exist_ok=True)

    cmd = ["west", "build", "-p", "-s", "zmk/app", "-d", str(build_dir), "-b", board]
    if snippet:
        cmd.extend(["-S", snippet])
    cmd.append("--")
    cmd.append(f"-DZMK_CONFIG={config_dir}")
    if shield:
        cmd.append(f"-DSHIELD={shield}")
    if extra_modules_dir is not None:
        cmd.append(f"-DZMK_EXTRA_MODULES={extra_modules_dir}")
    if cmake_args:
        cmd.extend(shlex.split(cmake_args))

    run(cmd, cwd=base_dir)

    zephyr_out = build_dir / "zephyr"
    uf2 = zephyr_out / "zmk.uf2"
    fallback = zephyr_out / f"zmk.{fallback_binary}"

    output_dir.mkdir(parents=True, exist_ok=True)
    if uf2.exists():
        dst = output_dir / f"{artifact}.uf2"
        shutil.copy2(uf2, dst)
        return dst
    if fallback.exists():
        dst = output_dir / f"{artifact}.{fallback_binary}"
        shutil.copy2(fallback, dst)
        return dst

    raise FileNotFoundError(
        f"No build artifact found for {artifact} (expected zmk.uf2 or zmk.{fallback_binary})."
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build firmware locally using the same steps as build-user-config.yml."
    )
    parser.add_argument("--build-matrix-path", default="build.yaml")
    parser.add_argument("--config-path", default="config")
    parser.add_argument("--fallback-binary", default="bin")
    parser.add_argument("--output-dir", default="firmware")
    parser.add_argument(
        "--artifact-names",
        default="",
        help=(
            "Comma-separated artifact-name values or wildcard patterns "
            "(e.g. 'totem_*', '*_reset'). If omitted, build all entries."
        ),
    )
    parser.add_argument(
        "--base-dir",
        default="/tmp/zmk-config",
        help="Base west workspace dir in container (mirrors CI temp dir behavior).",
    )
    parser.add_argument(
        "--zmk-revision",
        default="",
        help="Override only the `zmk` project revision in config/west.yml (e.g. main, v0.3).",
    )
    parser.add_argument(
        "--skip-update",
        action="store_true",
        help="Skip west update for faster incremental builds.",
    )
    parser.add_argument("--list", action="store_true", help="List artifact-name values and exit.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    build_matrix_path = (REPO_ROOT / args.build_matrix_path).resolve()
    src_config_path = (REPO_ROOT / args.config_path).resolve()
    output_dir = (REPO_ROOT / args.output_dir).resolve()
    base_dir = Path(args.base_dir).resolve()
    build_root = (REPO_ROOT / ".build" / "local" / "build").resolve()

    if not build_matrix_path.exists():
        raise FileNotFoundError(f"Build matrix path not found: {build_matrix_path}")
    if not src_config_path.exists():
        raise FileNotFoundError(f"Config path not found: {src_config_path}")

    entries = load_matrix(build_matrix_path)
    if not entries:
        raise ValueError(f"No matrix entries found in {build_matrix_path}")

    if args.list:
        print("Available artifact-name values:")
        for entry in entries:
            print(f"- {artifact_name(entry)}")
        return 0

    patterns = [part.strip() for part in args.artifact_names.split(",") if part.strip()]
    entries = filter_matrix(entries, patterns)

    # Mirror build-user-config.yml behavior:
    # if zephyr/module.yml exists in repo, build from isolated base_dir and load repo as extra module.
    if (REPO_ROOT / "zephyr" / "module.yml").exists():
        config_dir = ensure_config_copy(src_config_path, base_dir, src_config_path.name)
        # Stage the extra module into container-local /tmp to avoid host-mounted FS race issues.
        extra_modules_dir: Path | None = stage_extra_modules_from_git(REPO_ROOT, Path("/tmp"))
    else:
        base_dir = REPO_ROOT
        config_dir = src_config_path
        extra_modules_dir = None

    if args.zmk_revision.strip():
        override_zmk_revision(config_dir, args.zmk_revision.strip())

    ensure_west_ready(base_dir, config_dir, skip_update=args.skip_update)

    produced: list[Path] = []
    for entry in entries:
        name = artifact_name(entry)
        print(f"\n=== Building {name} ===", flush=True)
        out = build_entry(
            entry=entry,
            base_dir=base_dir,
            build_root=build_root,
            output_dir=output_dir,
            config_dir=config_dir,
            fallback_binary=args.fallback_binary,
            extra_modules_dir=extra_modules_dir,
        )
        produced.append(out)
        print(f"Built artifact: {out}", flush=True)

    print("\nBuild complete.", flush=True)
    for out in produced:
        print(f"- {out}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        print(f"Command failed: {exc}", file=sys.stderr)
        raise
