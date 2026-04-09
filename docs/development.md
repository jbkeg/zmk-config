# Development

This document describes day-to-day development and local build flow for this repository.

Related references:

- Known non-blocking warning tracker: `docs/known_issues.md`

## Branch Roles

Use these branch roles when choosing where to develop and test:

| Branch | Purpose |
| --- | --- |
| `main` | development |
| `canary` | latest |
| `v0.3` | versioned ZMK v0.3 maintenance branch |
| `scanner` | scanner |

## CI Workflows

Build and release are matrix-driven via `build.yaml`.

- `.github/workflows/build.yml`: the only reusable firmware build workflow; supports full matrix, filtered builds, and profile selection
- `.github/workflows/release.yml`: resolves `stable` or `canary` from the tag/branch (or manual override), then publishes firmware release assets
- `.github/workflows/run-tests.yml`: resolves the target ZMK version, patches the test manifest inside an isolated temporary workspace, and uploads build logs from the isolated build directory
- `.github/workflows/config-policy-guard.yml`: policy lint plus random matrix sanity builds through `build.yml`

## Recommended Workflow (GitHub Actions)

1. Edit `config/*.keymap`, `config/*.conf`, `build.yaml`, or shield files.
2. Commit and push your branch.
3. Wait for CI (`Build ZMK firmware` or test workflows).
4. Download build artifacts from Actions or release assets from Releases.
5. Flash matching firmware files to target devices.

This keeps builds aligned with pinned dependencies in `config/west.yml`.

## External Modules

The active non-versioning branches now depend on additional west modules for Raw HID and KeyPeek layer notifications:

- `zmk-raw-hid`
- `zmk-keypeek-layer-notifier`

If you switch to one of those branches locally after working on `v0.3`, run `west update` before building so the workspace matches the branch manifest.

## Configuration Policy (Split Role)

Use this layering to avoid split-side regressions and warning-only misconfigurations:

1. Board/shield role defaults:
   - Put side-specific role and transport defaults in board/shield defconfig files (`Kconfig.defconfig`, `*_defconfig`).
   - Examples: `CONFIG_ZMK_USB`, `CONFIG_ZMK_BLE`, split role flags.
2. Side overlay/conf overrides:
   - Keep side-only overrides in side-specific files (`*_left.conf`, `*_right.conf`) only when needed.
3. User config (`config/*.conf`):
   - Keep this layer side-neutral.
   - Do not set split role or transport ownership here.
4. Shared snippet config (`snippets/common-config/common-config.conf`):
   - Keep this hardware-agnostic.
   - Do not force hardware-specific options globally (for example global `CONFIG_SPI=y`).
5. Shared config references:
   - `snippets/common-config/extra-config.conf` is a commented copy/paste reference.
   - Keep it as reference-only; do not wire it as a global snippet input.

Guardrails:

- `.github/workflows/config-policy-guard.yml` enforces the policy on push/PR.
- The guard runs static policy checks and a lightweight right-side CI build sanity pass.

## Local Build (Docker, CI-like)

Two local services are provided in `docker-compose.yml`:

- `zmk-build-stable`: uses `zmkfirmware/zmk-build-arm:3.5` for the stable ZMK `v0.3` / Zephyr `3.5` line.
- `zmk-build-canary`: uses `zmkfirmware/zmk-build-arm:4.1-branch` for the canary ZMK `main` / Zephyr `4.1` line.

Note: the image tag must still match the intended ZMK/Zephyr line. In this repo, `stable` maps to ZMK `v0.3` / Zephyr `3.5`, while `canary` maps to ZMK `main` / Zephyr `4.1`.

### Prerequisites

- Docker (Docker Desktop or Docker Engine)
- Repository cloned locally

### Short, cross-platform command (recommended)

From repository root:

```bash
# List valid artifact-name values from build.yaml
docker compose run --rm zmk-build-stable --list

# Build selected targets
docker compose run --rm zmk-build-stable --artifact-names totem_left,totem_right,totem_reset

# Build with wildcard patterns (shell-style)
docker compose run --rm zmk-build-stable --artifact-names "totem_*"
docker compose run --rm zmk-build-stable --artifact-names "*_left,*_right"

# Build in parallel (up to 3 targets at a time)
docker compose run --rm zmk-build-stable --artifact-names "totem_*" --jobs 3

# Build every target in build.yaml
docker compose run --rm zmk-build-stable

# Build against the canary ZMK main line
docker compose run --rm zmk-build-canary --artifact-names totem_left
```

Notes:

- This uses `docker-compose.yml`, `scripts/build_profiles.py`, and `scripts/build_runner.py`.
- Output artifacts are written to `firmware/`.
- Build directories are kept under `.build/local/build/`.
- West workspace/cache state is kept under `.build/local/workspace/` (stable) and `.build/local/workspace-main/` (canary).
- `--artifact-names` accepts exact names and wildcard patterns. If a pattern matches nothing, the script exits with an error.
- `--jobs` controls matrix-level parallelism.
- If `--jobs` is omitted, it auto-selects `min(selected entries, max(1, physical core count // 2))`.
- Even when `--jobs` is provided, the runner caps it to physical core count.

### Direct docker run (without compose)

If you prefer not to use Docker Compose:

```bash
docker run --rm -it -v "${PWD}:/workspace" -w /workspace zmkfirmware/zmk-build-arm:3.5 python3 scripts/build_runner.py build-many --profile stable --artifact-names "totem_left,totem_right"

# Parallel example
docker run --rm -it -v "${PWD}:/workspace" -w /workspace zmkfirmware/zmk-build-arm:3.5 python3 scripts/build_runner.py build-many --profile stable --artifact-names "totem_*" --jobs 3
```

### Why not plain CMake?

Use `west build` instead of raw `cmake` for ZMK firmware. `west` handles:

- Zephyr/ZMK workspace initialization
- module resolution from `config/west.yml`
- snippet wiring and board/shield build conventions

The local runner follows the same model as the GitHub workflow and keeps command length short.

## Flashing

For each target device:

1. Connect via USB.
2. Enter bootloader mode (usually double-tap reset).
3. Copy the matching `.uf2` file to the mounted drive.
4. Wait for automatic reboot.

## Quick Troubleshooting

- Unknown `artifact-name`: run `--list` and use an exact name or valid wildcard from `build.yaml`.
- Missing module/build errors: rerun without `--skip-update` so `west update` runs.
- `recursive 'source' of 'Kconfig.zephyr' detected`: this usually means a local Zephyr checkout exists under repo `zephyr/`. The local runner now stages only git-visible module files, but cleanup of stale local checkouts still helps (`zephyr/`, `modules/`, `.west/`).
- No `.uf2` output for a target: check for fallback binary output (`.bin`), board type, and build logs.
- Split reconnect problems after flashing: flash reset firmware and re-pair.
