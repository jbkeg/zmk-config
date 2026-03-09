# Urchin 🪸

![Urchin Thumbnail](/docs/images/urchin_thumbnail.jpg)

This document describes the Urchin keyboard: its hardware, design philosophy, layout, and how ZMK firmware applies to it.

The Urchin keyboard was originally designed by Duccio (duckyb) as a 34-key wireless-only split keyboard optimized for ZMK and nice!nano controllers. It is a derivative of the Sweep/Swoop family with native support for nice!view displays and hotswappable sockets.

## Support Snapshot

Implemented matrix targets:

| Target | Board | Shield | Snippet | Artifact Name | Status |
| --- | --- | --- | --- | --- | --- |
| Left half (direct split) | `nice_nano_v2` | `urchin_left nice_view_adapter nice_view_gem` | `common-config studio-rpc-usb-uart` | `urchin_left` | Active |
| Right half | `nice_nano_v2` | `urchin_right nice_view_adapter nice_view_gem` | none | `urchin_right` | Active |
| Left half (dongle split) | `nice_nano_v2` | `urchin_left_w_dongle nice_view_adapter nice_view_gem` | none | `urchin_left_w_dongle` | Active |
| Dongle (ZDD) | `nice_nano_v2` | `urchin_dongle zdd_adapter dongle_display` | `studio-rpc-usb-uart` | `urchin_zdd_dongle` | Active |
| Keyboard reset | `nice_nano_v2` | `settings_reset` | none | `urchin_reset` | Active |
| Dongle reset | `nice_nano_v2` | `settings_reset` | none | `urchin_zdd_dongle_reset` | Active |

## Reference Material

- Original Urchin hardware and firmware: <https://github.com/duckyb/urchin>
  - Original makers firmware: <https://github.com/duckyb/urchin-zmk-firmware>
  - Original makers shield: <https://github.com/duckyb/urchin-zmk-module>
- Variant ZMK configurations and community forks: <https://github.com/theearp/zmk-urchin>

## Hardware Overview

- 34-key split matrix (3 rows of 10 keys per half plus thumb cluster)
- In this repo, direct split mode uses USB host connection on the left half
- Dongle split mode uses BLE host pairing through `urchin_zdd_dongle`
- Kailh Choc v1 hotswap sockets for low-profile switches
- Designed with power savings and deep sleep in mind
- Support for optional nice!view displays (sharp memory-in-pixel)
- Custom PCB with diodes and matrix for ZMK compatibility

## Layout

### Physical Layout

The Urchin uses a compact 3x5+2 split layout per half with a thumb cluster.

![Urchin Render](/docs/images/urchin_render.png)

![Urchin Layout](/docs/images/urchin_layout.svg)

### Keymap

Urchin keymaps often use layer modifiers under the thumbs to access numbers, symbols, and navigation.

![Urchin Keymap](/docs/images/urchin_keymap.svg)

## Firmware Structure

The original ZMK firmware for Urchin includes:

- Matrix definitions for the split 34-key layout
- Bluetooth configuration for nice!nano
- Optional display support for nice!view screens
- Layer and behavior definitions matching the physical layout

Community forks modify keymaps and layer logic, but the core hardware support remains in the original repo structure.

Implemented paths in this repo:

- `boards/shields/urchin/`
- `config/urchin.keymap`
- `config/urchin.conf`
- `build.yaml`

Dongle split targets reuse the same `config/urchin.keymap` and `config/urchin.conf`. No separate dongle keymap file is required.

## How to Use

### Build

1. Use this repo's Urchin integration.
2. Adjust `config/urchin.conf` for features like sleep, display, and Bluetooth power.
3. Customize `config/urchin.keymap` for your preferred layers.
4. Build using GitHub Actions or local Docker.

Local Docker (recommended):

```bash
# list artifacts
docker compose run --rm zmk-build-stable --list

# build direct split targets
docker compose run --rm zmk-build-stable --artifact-names urchin_left,urchin_right,urchin_reset

# build dongle split targets
docker compose run --rm zmk-build-stable --artifact-names urchin_left_w_dongle,urchin_right,urchin_zdd_dongle,urchin_zdd_dongle_reset,urchin_reset
```

### Flashing

Direct split (`urchin_left` + `urchin_right`):

1. Connect a half to the PC via USB and enter bootloader mode.
2. Optional: flash `urchin_reset.uf2` if you need to clear settings/bonds.
3. Flash `urchin_left.uf2` to the left half.
4. Flash `urchin_right.uf2` to the right half.
5. Power-cycle both halves.

Dongle split (`urchin_zdd_dongle` + `urchin_left_w_dongle` + `urchin_right`), clean start recommended:

1. Flash reset firmware first:
   - `urchin_zdd_dongle_reset.uf2` to the dongle.
   - `urchin_reset.uf2` to both keyboard halves.
2. Flash runtime firmware:
   - `urchin_zdd_dongle.uf2` to the dongle.
   - `urchin_left_w_dongle.uf2` to the left half.
   - `urchin_right.uf2` to the right half.
3. Remove old dongle bond on the host, then pair the host to the dongle again.
4. Power-cycle dongle and both halves if split links do not reconnect immediately.

Artifact-to-device mapping:

| Artifact | Flash To |
| --- | --- |
| `urchin_left.uf2` | Left half (direct split) |
| `urchin_left_w_dongle.uf2` | Left half (dongle split) |
| `urchin_right.uf2` | Right half |
| `urchin_zdd_dongle.uf2` | Dongle |
| `urchin_reset.uf2` | Keyboard half for clearing settings/bonds |
| `urchin_zdd_dongle_reset.uf2` | Dongle for clearing settings/bonds |

## Display and Power

- Nice!view displays provide battery, connection, and layer status if installed.
- Power usage is optimized for long battery life using deep sleep.

## Typical Use Case

Urchin is used by split keyboard enthusiasts who want:

- Wireless Bluetooth connection
- Compact ergonomic layout without a number row
- Layer-based number and symbol access
- Display feedback for connection and battery status

Many users report the split 3x5 layout feels fast once the muscle memory develops.

## Troubleshooting

- If dongle is connected to host but halves do not connect, stale split bonds are the most common cause.
- For stale split bonds, run full reset-first sequence on dongle and both halves, then flash runtime firmware again.
- If BLE pairing fails after reflashing, remove host bond for the dongle and pair again.
- If one half behaves differently, reflash both halves from the same build batch.
- If display status is missing, verify `nice_view_adapter nice_view_gem` are still in the shield list for Urchin targets in `build.yaml`.
- If Studio does not connect on left side, confirm `urchin_left` keeps `common-config studio-rpc-usb-uart`.

## Status

- Urchin split targets are active in `build.yaml`.
- Urchin dongle-related targets are active in `build.yaml`.
