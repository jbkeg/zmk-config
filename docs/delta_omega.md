# Delta Omega

![Delta Omega](/docs/images/delta_omega_header.png)

This document covers Delta Omega support as integrated in this repository.

## Support Snapshot

Implemented matrix targets:

| Target | Board | Shield | Snippet | Artifact Name | Status |
| --- | --- | --- | --- | --- | --- |
| Left half (direct split) | `xiao_ble//zmk` | `delta_omega_left` | `common-config studio-rpc-usb-uart` | `delta_omega_left` | Active |
| Right half | `xiao_ble//zmk` | `delta_omega_right` | none | `delta_omega_right` | Active |
| Left half (dongle split) | `xiao_ble//zmk` | `delta_omega_left_w_dongle` | none | `delta_omega_left_w_dongle` | Active |
| Dongle (single keyboard) | `nice_nano//zmk` | `delta_omega_dongle zdd_adapter dongle_display` | `studio-rpc-usb-uart` | `delta_omega_zdd_dongle` | Active |
| Keyboard reset | `xiao_ble//zmk` | `settings_reset` | none | `delta_omega_reset` | Active |
| Dongle reset | `nice_nano//zmk` | `settings_reset` | none | `delta_omega_zdd_dongle_reset` | Active |

## Reference Material

- Delta Omega hardware: <https://github.com/unspecworks/delta-omega>
- Delta Omega ZMK module: <https://github.com/unspecworks/zmk-keyboard-delta-omega>
- ZMK docs: <https://zmk.dev/docs>

## Hardware Overview

- 34-key (3x5+2) split keyboard
- Ultra-low-profile design
- In this repo, direct split mode uses USB host connection on the left half
- Dongle split mode uses BLE host pairing through `delta_omega_zdd_dongle`
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

- `modules/keyboards/delta-omega/boards/shields/delta_omega/` (upstream historical reference)
- Variant-specific shield split is not present in this repo today; new variants should be added under `boards/shields/delta_omega/`.

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
docker compose run --rm zmk-build-stable --list

# build direct split targets
docker compose run --rm zmk-build-stable --artifact-names delta_omega_left,delta_omega_right,delta_omega_reset

# build dongle split targets
docker compose run --rm zmk-build-stable --artifact-names delta_omega_left_w_dongle,delta_omega_right,delta_omega_zdd_dongle,delta_omega_zdd_dongle_reset,delta_omega_reset
```

CI/GitHub Actions:

1. Push changes.
2. Run matrix build workflow.
3. Download artifacts for the topology you flash.

### Flashing

Direct split (`delta_omega_left` + `delta_omega_right`):

1. Put each keyboard half into bootloader mode.
2. Optional: flash `delta_omega_reset.uf2` if you need to clear settings/bonds.
3. Flash `delta_omega_left.uf2` to the left half.
4. Flash `delta_omega_right.uf2` to the right half.
5. Power-cycle both halves.

Dongle split (`delta_omega_zdd_dongle` + `delta_omega_left_w_dongle` + `delta_omega_right`), clean start recommended:

1. Flash reset firmware first:
   - `delta_omega_zdd_dongle_reset.uf2` to the dongle.
   - `delta_omega_reset.uf2` to both keyboard halves.
2. Flash runtime firmware:
   - `delta_omega_zdd_dongle.uf2` to the dongle.
   - `delta_omega_left_w_dongle.uf2` to the left half.
   - `delta_omega_right.uf2` to the right half.
3. Remove old dongle bond on the host, then pair the host to the dongle again.
4. Power-cycle dongle and both halves if split links do not reconnect immediately.

Artifact-to-device mapping:

| Artifact | Flash To |
| --- | --- |
| `delta_omega_left.uf2` | Left half (direct split) |
| `delta_omega_left_w_dongle.uf2` | Left half (dongle split) |
| `delta_omega_right.uf2` | Right half |
| `delta_omega_zdd_dongle.uf2` | Dongle |
| `delta_omega_reset.uf2` | Keyboard half for clearing settings/bonds |
| `delta_omega_zdd_dongle_reset.uf2` | Dongle for clearing settings/bonds |

## Troubleshooting

- Build cannot find target:
  - Run `docker compose run --rm zmk-build-stable --list` and confirm artifact names.
- If dongle is connected to host but halves do not connect, stale split bonds are the most common cause.
- For stale split bonds, run full reset-first sequence on dongle and both halves, then flash runtime firmware again.
- If BLE pairing fails after reflashing, remove host bond for the dongle and pair again.
- Wrong behavior after flashing one side:
  - Reflash left and right from the same CI/local build batch.
- Studio connection issue on left build:
  - Confirm `common-config studio-rpc-usb-uart` is still applied for `delta_omega_left` in `build.yaml`.

## Status

- Delta Omega split support is active with in-repo shield/config wiring.
- Build matrix entries are present for direct and dongle topologies, including reset artifacts.
- Delta Omega dongle-related targets are active in `build.yaml`.
