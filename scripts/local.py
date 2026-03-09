#!/usr/bin/env python3
"""Compatibility wrapper for the shared build runner."""

from __future__ import annotations

import argparse

import build_runner


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build firmware locally using the shared GitHub/local runner."
    )
    parser.add_argument("--build-matrix-path", default="build.yaml")
    parser.add_argument("--build-matrix-json", default="")
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
    parser.add_argument("--base-dir", default="")
    parser.add_argument(
        "--zmk-revision",
        default="",
        help="Optional override for the `zmk` project revision in config/west.yml.",
    )
    parser.add_argument("--skip-update", action="store_true")
    parser.add_argument(
        "--jobs",
        type=int,
        default=None,
        help=(
            "Number of matrix entries to build in parallel. "
            "Default: auto (min(selected entries, max(1, physical core count // 2)))."
        ),
    )
    parser.add_argument("--list", action="store_true")
    parser.add_argument(
        "--profile",
        default="stable",
        help="Build profile. If omitted, defaults to stable unless --zmk-revision main is set.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    profile = args.profile
    if args.zmk_revision.strip().lower() == "main" and args.profile == "stable":
        profile = "canary"

    forwarded_args = [
        "build-many",
        "--profile",
        profile,
        "--build-matrix-path",
        args.build_matrix_path,
        "--build-matrix-json",
        args.build_matrix_json,
        "--config-path",
        args.config_path,
        "--fallback-binary",
        args.fallback_binary,
        "--output-dir",
        args.output_dir,
        "--artifact-names",
        args.artifact_names,
    ]

    if args.base_dir:
        forwarded_args.extend(["--base-dir", args.base_dir])
    if args.zmk_revision:
        forwarded_args.extend(["--zmk-revision-override", args.zmk_revision])
    if args.skip_update:
        forwarded_args.append("--skip-update")
    if args.jobs is not None:
        forwarded_args.extend(["--jobs", str(args.jobs)])
    if args.list:
        forwarded_args.append("--list")

    return build_runner.main(forwarded_args)


if __name__ == "__main__":
    raise SystemExit(main())
