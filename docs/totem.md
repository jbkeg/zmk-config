# TOTEM

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="/docs/images/totem_logo_dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="/docs/images/totem_logo_light.svg">
  <img alt="TOTEM logo font" src="/docs/images/totem_logo_light.svg">
</picture>

This document defines the ZMK configuration for the Totem keyboard as implemented in this repository. It assumes familiarity with ZMK, split keyboard firmware, and BLE behavior.

TOTEM is a 38-key column-staggered split keyboard. In this repository it is treated strictly as a ZMK-based, BLE peripheral device. Typical builds use a XIAO BLE with a UF2-capable bootloader.

## Support Snapshot

Implemented matrix targets:

| Target | Board | Shield | Snippet | Artifact Name | Status |
| --- | --- | --- | --- | --- | --- |
| Left half | `seeeduino_xiao_ble` | `totem_left` | `common-config studio-rpc-usb-uart` | `totem_left` | Active |
| Right half | `seeeduino_xiao_ble` | `totem_right` | none | `totem_right` | Active |
| Reset | `seeeduino_xiao_ble` | `settings_reset` | none | `totem_reset` | Active |

Planned targets (not active in current build matrix):

- `totem_dongle`
- `totem_left_w_dongle`

## Reference Material

- Build Guide: [https://github.com/GEIGEIGEIST/totem](https://github.com/GEIGEIGEIST/totem)
  Hardware files and physical build instructions.
- QMK Config: [https://github.com/GEIGEIGEIST/qmk-config-totem](https://github.com/GEIGEIGEIST/qmk-config-totem)
  Reference implementation for QMK only. Not directly applicable to ZMK behavior.

## Hardware Overview

- 38-key column-staggered split keyboard
- Typical controller: XIAO BLE
- BLE-first usage model for split operation

## Layout

### Physical Layout

Physical switch arrangement. Visual reference only.

![TOTEM layout](/docs/images/totem_layout.svg)

### Keymap

![TOTEM keymap](/docs/images/totem_keymap.svg)

## Firmware Structure

TOTEM uses a split shield with a shared matrix transform and side-specific GPIO overlays.

Implemented paths:

- `boards/shields/totem/`
  Hardware definition, matrix transform, overlays, and metadata.
- `config/totem.conf`
  User-level feature and system configuration.
- `config/totem.keymap`
  Authoritative keymap. Layers, behaviors, HRM, combos, macros.
- `build.yaml`
  CI/local artifact matrix entries.

Planned/legacy references kept for continuity:

- `config/totem_dongle.keymap` (planned target path)

The shield-level keymap under `boards/shields/totem/` is treated as a factory fallback only. It is not intended for customization.

## Operational Constraints

- TOTEM operates only as a BLE peripheral.
- It cannot act as a BLE central.
- BLE role selection is compile-time.
- When used with a dongle, direct host BLE pairing is disabled.
- Switching BLE topology requires reflashing and rebonding.
- All global BLE and dongle constraints defined in the root README apply without exception.

## Non-Goals

- USB HID operation.
- Wired split communication.
- Runtime BLE role or topology switching.
- Mixed transport modes.

## How to Use

### Build

1. Fork and clone the repository.
2. Modify `config/totem.keymap` and `config/totem.conf`.
3. Build using CI or local Docker.
4. Download artifacts for the target you flash.

Local Docker (recommended):

```bash
# list artifacts
docker compose run --rm zmk-build-release --list

# build only Totem targets
docker compose run --rm zmk-build-release --artifact-names totem_left,totem_right,totem_reset
```

Expected active artifacts:

- `totem_left.uf2`
- `totem_right.uf2`
- `totem_reset.uf2`

### Flashing

Assumes XIAO BLE with UF2 bootloader.

1. Connect the left half to the PC via USB.
2. Double-tap reset to enter bootloader mode.
3. Optional: flash `totem_reset.uf2` to clear state.
4. Copy `totem_left.uf2` to the mounted drive.
5. Repeat for the right half using `totem_right.uf2`.
6. Disconnect USB and power halves normally.

Artifact-to-device mapping:

| Artifact | Flash To |
| --- | --- |
| `totem_left.uf2` | Left half |
| `totem_right.uf2` | Right half |
| `totem_reset.uf2` | Any side when clearing settings/bonds |

## Configuration

### `config/totem.conf`

User-level system configuration. Typical concerns include BLE behavior, sleep tuning, and feature flags.

Example baseline:

```conf
# Totem user configuration

# Bluetooth
CONFIG_ZMK_BLE=y
CONFIG_ZMK_BLE_CLEAR_BONDS_ON_STARTUP=n

# Power management
CONFIG_ZMK_SLEEP=y
CONFIG_ZMK_IDLE_SLEEP_TIMEOUT=600000

# Optional tooling support
CONFIG_ZMK_STUDIO=y
```

Notes:

- ZMK Studio support is optional.
- Enabling Studio increases firmware size and may affect power usage.
- Adjust values based on battery behavior and usage patterns.

### `config/totem.keymap`

Authoritative keymap definition.

Rules:

- All layout logic lives here.
- HRM, combos, macros, and layers are defined here.
- Combo positions must align with the matrix transform defined in `boards/shields/totem/totem.dtsi`.
- Avoid editing shield-level keymaps unless redefining factory defaults.

No changes are required if the current layout matches intended behavior.

## Troubleshooting

- If halves do not connect, flash `totem_reset.uf2` and then reflash both sides.
- If BLE pairing fails, remove host bonds and re-pair after reflashing.
- Uneven sleep or wake behavior usually indicates mismatched firmware batch or stale state.
- If Studio does not connect on left side, confirm `totem_left` still uses `common-config studio-rpc-usb-uart` in `build.yaml`.

Successful operation is indicated by stable split communication followed by host BLE connection.

## Status

- Totem split targets are active in `build.yaml`.
- Dongle-related Totem targets are documented as planned follow-up.
- Canonical reference for Totem within this repository.
