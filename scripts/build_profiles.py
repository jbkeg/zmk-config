#!/usr/bin/env python3
"""Shared build profile definitions for local Docker and GitHub Actions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


PROFILES: dict[str, dict[str, str]] = {
    "stable": {
        "profile": "stable",
        "container_image": "zmkfirmware/zmk-build-arm:3.5",
        "zmk_revision": "v0.3",
        "base_dir": "/tmp/zmk-config",
        "workspace_dir": ".build/local/workspace",
        "cache_key": "stable-3.5-v0.3",
    },
    "canary": {
        "profile": "canary",
        "container_image": "zmkfirmware/zmk-build-arm:4.1-branch",
        "zmk_revision": "main",
        "base_dir": "/tmp/zmk-config-main",
        "workspace_dir": ".build/local/workspace-main",
        "cache_key": "canary-4.1-branch",
    },
}


def get_profile(name: str) -> dict[str, str]:
    profile_name = name.strip().lower()
    try:
        return dict(PROFILES[profile_name])
    except KeyError as exc:
        valid = ", ".join(sorted(PROFILES))
        raise ValueError(f"Unknown profile '{name}'. Valid profiles: {valid}.") from exc


def write_github_outputs(path: Path, values: dict[str, str]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        for key, value in values.items():
            handle.write(f"{key}={value}\n")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    resolve = subparsers.add_parser("resolve-profile", help="Resolve a named build profile.")
    resolve.add_argument("--profile", default="stable", help="Profile name: stable or canary.")
    resolve.add_argument(
        "--github-output",
        default="",
        help="Write resolved profile fields to the provided GITHUB_OUTPUT file.",
    )

    subparsers.add_parser("list-profiles", help="List available build profiles.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.command == "list-profiles":
        for profile_name in sorted(PROFILES):
            print(profile_name)
        return 0

    profile = get_profile(args.profile)
    if args.github_output:
        write_github_outputs(Path(args.github_output), profile)
    print(json.dumps(profile, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
