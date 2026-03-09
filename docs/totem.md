# TOTEM

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="/docs/images/totem_logo_dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="/docs/images/totem_logo_light.svg">
  <img alt="TOTEM logo font" src="/docs/images/totem_logo_light.svg">
</picture>

This document defines the ZMK configuration for the Totem keyboard as implemented in this repository. It assumes familiarity with ZMK, split keyboard firmware, and BLE behavior.

TOTEM is a 38-key column-staggered split keyboard. This repository supports both direct split operation and dongle-based split operation.

## Support Snapshot

Implemented matrix targets:

| Target                   | Board                | Shield                                    | Snippet                             | Artifact Name            | Status |
| ------------------------ | -------------------- | ----------------------------------------- | ----------------------------------- | ------------------------ | ------ |
| Left half (direct split) | `xiao_ble//zmk` | `totem_left`                              | `common-config studio-rpc-usb-uart` | `totem_left`             | Active |
| Right half               | `xiao_ble//zmk` | `totem_right`                             | none                                | `totem_right`            | Active |
| Left half (dongle split) | `xiao_ble//zmk` | `totem_left_w_dongle`                     | none                                | `totem_left_w_dongle`    | Active |
| Dongle (ZDD)             | `nice_nano//zmk`       | `totem_dongle zdd_adapter dongle_display` | `studio-rpc-usb-uart`               | `totem_zdd_dongle`       | Active |
| Keyboard reset           | `xiao_ble//zmk` | `settings_reset`                          | none                                | `totem_reset`            | Active |
| Dongle reset (ZDD)       | `nice_nano//zmk`       | `settings_reset`                          | none                                | `totem_zdd_dongle_reset` | Active |

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

The shield-level keymap under `boards/shields/totem/` is treated as a factory fallback only. It is not intended for customization.

## Operational Constraints

- BLE role and split topology are compile-time decisions.
- In dongle topology, `totem_zdd_dongle` is the split BLE hub endpoint and both keyboard halves are peripherals.
- When used with a dongle topology, direct host pairing for keyboard halves is not used.
- Switching topology requires reflashing and rebonding.
- `CONFIG_ZMK_BLE_CLEAR_BONDS_ON_START` is disabled in shared config, so stale bonds persist until explicit reset/clear.
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
docker compose run --rm zmk-build-stable --list

# build direct split targets
docker compose run --rm zmk-build-stable --artifact-names totem_left,totem_right,totem_reset

# build dongle split targets
docker compose run --rm zmk-build-stable --artifact-names totem_left_w_dongle,totem_right,totem_zdd_dongle,totem_zdd_dongle_reset,totem_reset
```

Expected active artifacts:

- `totem_left.uf2`
- `totem_left_w_dongle.uf2`
- `totem_right.uf2`
- `totem_zdd_dongle.uf2`
- `totem_reset.uf2`
- `totem_zdd_dongle_reset.uf2`

### Flashing

Assumes XIAO BLE for halves and nice!nano v2 for dongle, all with UF2 bootloader support.

Direct split (`totem_left` + `totem_right`):

1. Connect a half to the PC via USB and enter bootloader mode.
2. Optional: flash `totem_reset.uf2` if you need to clear settings/bonds.
3. Flash `totem_left.uf2` to the left half.
4. Flash `totem_right.uf2` to the right half.
5. Power-cycle both halves.

Dongle split (`totem_zdd_dongle` + `totem_left_w_dongle` + `totem_right`), clean start recommended:

1. Flash reset firmware first:
   - `totem_zdd_dongle_reset.uf2` to the dongle.
   - `totem_reset.uf2` to both keyboard halves.
2. Flash runtime firmware:
   - `totem_zdd_dongle.uf2` to the dongle.
   - `totem_left_w_dongle.uf2` to the left half.
   - `totem_right.uf2` to the right half.
3. Remove old dongle bond on the host, then pair the host to the dongle again.
4. Power-cycle dongle and both halves if split links do not reconnect immediately.

Artifact-to-device mapping:

| Artifact                     | Flash To                                  |
| ---------------------------- | ----------------------------------------- |
| `totem_left.uf2`             | Left half (direct split)                  |
| `totem_left_w_dongle.uf2`    | Left half (dongle split)                  |
| `totem_right.uf2`            | Right half                                |
| `totem_zdd_dongle.uf2`       | Dongle                                    |
| `totem_reset.uf2`            | Keyboard half for clearing settings/bonds |
| `totem_zdd_dongle_reset.uf2` | Dongle for clearing settings/bonds        |

## Configuration

### `config/totem.conf`

User-level system configuration. Typical concerns include BLE behavior, sleep tuning, and feature flags.

Example baseline:

```conf
# Totem user configuration

# Bluetooth
CONFIG_ZMK_BLE=y
CONFIG_ZMK_BLE_CLEAR_BONDS_ON_START=n

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

- If dongle is connected to host but halves do not connect, stale split bonds are the most common cause.
- For stale split bonds, run full reset-first sequence on dongle and both halves, then flash runtime firmware again.
- If BLE pairing fails after reflashing, remove host bond for the dongle and pair again.
- Uneven sleep or wake behavior usually indicates mismatched firmware batch or stale state.
- If Studio does not connect on left side, confirm `totem_left` still uses `common-config studio-rpc-usb-uart` in `build.yaml`.

Successful operation is indicated by stable split communication followed by stable host connection for the selected topology.

## Status

- Totem split targets are active in `build.yaml`.
- Totem dongle-related targets are active in `build.yaml`.
- Canonical reference for Totem within this repository.
