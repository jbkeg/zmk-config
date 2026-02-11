# Delta Omega

![Delta Omega](/docs/images/delta_omega_header.png)

This document covers Delta Omega support as integrated in this repository.

## Support Snapshot

Implemented matrix targets:

| Target | Board | Shield | Snippet | Artifact Name | Status |
| --- | --- | --- | --- | --- | --- |
| Left half | `seeeduino_xiao_ble` | `delta_omega_left` | `common-config studio-rpc-usb-uart` | `delta_omega_left` | Active |
| Right half | `seeeduino_xiao_ble` | `delta_omega_right` | none | `delta_omega_right` | Active |
| Reset | `seeeduino_xiao_ble` | `settings_reset` | none | `delta_omega_reset` | Active |

Planned targets (not active in current build matrix):

| Target | Planned Artifact Name | Status |
| --- | --- | --- |
| Dongle | `delta_omega_dongle` | Planned |
| Left with dongle | `delta_omega_left_w_dongle` | Planned |

## Reference Material

- Delta Omega hardware: <https://github.com/unspecworks/delta-omega>
- Delta Omega ZMK module: <https://github.com/unspecworks/zmk-keyboard-delta-omega>
- ZMK docs: <https://zmk.dev/docs>

## Hardware Overview

- 34-key (3x5+2) split keyboard
- Ultra-low-profile design
- Upstream references exist; this repo currently keeps Delta Omega shield/config files in-tree

## Layout

### Physical Layout

![Delta Omega dimension](/docs/images/delta_omega_dimension.png)
![Delta Omega splay](/docs/images/delta_omega_splay_layout.png)
![Delta Omega layout](/docs/images/delta_omega_layout.svg)

### Keymap

![Delta Omega keymap](/docs/images/delta_omega_keymap.svg)

## Firmware Structure

Implemented paths in this repo:

- `boards/shields/delta_omega/`
- `config/delta_omega.keymap`
- `config/delta_omega.conf`
- `config/delta_omega.json`
- `build.yaml`
- `config/west.yml`

Planned/legacy references kept for continuity:

- `config/delta_omega_dongle.keymap` (planned target path)
- `modules/keyboards/delta-omega/boards/shields/delta_omega/` (upstream historical reference)
- `boards/shields/delta_omega_variants/` (planned variants path)

## How to Use

### Build

1. Ensure dependencies are updated:

```bash
west update
```

2. Edit behavior in:
   - `config/delta_omega.keymap`
   - `config/delta_omega.conf`
3. Build with matrix artifact names from `build.yaml`.

Local Docker (recommended):

```bash
# list artifacts
docker compose run --rm zmk-build-release --list

# build only Delta Omega targets
docker compose run --rm zmk-build-release --artifact-names delta_omega_left,delta_omega_right,delta_omega_reset
```

CI/GitHub Actions:

1. Push changes.
2. Run matrix build workflow.
3. Download `delta_omega_left`, `delta_omega_right`, `delta_omega_reset` artifacts.

### Flashing

1. Put the target board into bootloader mode (double-reset).
2. Flash matching UF2 for each side.
3. For split operation, flash both halves from the same build batch.
4. If BLE state is stale, flash reset firmware and re-pair.

Artifact-to-device mapping:

| Artifact | Flash To |
| --- | --- |
| `delta_omega_left.uf2` | Left half |
| `delta_omega_right.uf2` | Right half |
| `delta_omega_reset.uf2` | Any side when clearing settings/bonds |

## Troubleshooting

- Build cannot find target:
  - Run `docker compose run --rm zmk-build-release --list` and confirm artifact names.
- Flash appears successful but split does not reconnect:
  - Flash `delta_omega_reset` on both halves, then re-pair.
- Wrong behavior after flashing one side:
  - Reflash left and right from the same CI/local build batch.
- Studio connection issue on left build:
  - Confirm `common-config studio-rpc-usb-uart` is still applied for `delta_omega_left` in `build.yaml`.

## Status

- Delta Omega split support is active with in-repo shield/config wiring.
- Build matrix entries are present for `delta_omega_left`, `delta_omega_right`, and `delta_omega_reset`.
- Dongle-related targets and variants references are documented as planned follow-up.
