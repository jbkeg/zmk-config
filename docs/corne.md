# Corne

![Corne thumbnail](/docs/images/corne_thumbnail.jpg)

This document describes Corne support in this repository and how to use it with the Continuum keymap framework.

Corne (crkbd) is a column-staggered split keyboard family commonly used in 3x6+3 (42-key) and 3x5+3 (36-key) layouts.

## Reference Material

- Corne hardware project: <https://github.com/foostan/crkbd>
- ZMK docs: <https://zmk.dev/docs>

## Hardware Overview

- Split ergonomic keyboard with column stagger
- Common variants:
  - 42 keys (3x6+3)
  - 36 keys (3x5+3)
- Typical ZMK builds use nice!nano-class controllers
- Many community variants add encoders, displays, or joystick hardware

## Layout

### Physical Layout

42-key Corne (3x6+3):

![Corne 3x6 layout](/docs/images/corne_3x6_layout.svg)

36-key Corne (3x5+3):

![Corne 3x5 layout](/docs/images/corne_3x5_layout.svg)

Eyelash Corne variants in this repo include extra matrix positions for joystick and encoder hardware.

### Keymap

Corne keymap logic is expected to come from `config/continuum/base.keymap`.

![Corne keymap](/docs/images/corne_keymap.svg)

You select the physical mapping by choosing the appropriate matrix header (`36.h`, `42.h`, `eyelash_corne36.h`, `eyelash_corne42.h`).

## Corne Mapping in This Repo

This repository provides Corne mappings through Continuum matrix headers:

- `config/continuum/matrix/36.h`
  - Generic 36-key mapping.
- `config/continuum/matrix/42.h`
  - Generic 42-key mapping.
- `config/continuum/matrix/eyelash_corne36.h`
  - 36-key Corne-style mapping with encoder/joystick positions.
- `config/continuum/matrix/eyelash_corne42.h`
  - 42-key Corne-style mapping with encoder/joystick positions.

## Firmware Structure

Relevant paths for Corne integration:

- `docs/corne.md`
  - This document
- `docs/continuum.md`
  - Continuum framework documentation
- `config/continuum/base.keymap`
  - Shared layers and behaviors
- `config/continuum/utils/helper.h`
  - Shared macro helpers and behavior utilities
- `config/continuum/matrix/36.h`
  - 36-key position mapping
- `config/continuum/matrix/42.h`
  - 42-key position mapping
- `config/continuum/matrix/eyelash_corne36.h`
  - 36-key Corne variant mapping (encoder/joystick)
- `config/continuum/matrix/eyelash_corne42.h`
  - 42-key Corne variant mapping (encoder/joystick)
- `config/eyelash_corne.keymap`
  - Eyelash Corne variation keymap using `eyelash_corne42.h`
- `config/eyelash_corne.conf`
  - Eyelash Corne variation baseline config overrides

## How to Use

### Keymap Setup

Create `config/corne.keymap` and include Continuum.

Example for 42-key Corne:

```c
#define CONFIG_WIRELESS
#include "continuum/matrix/42.h"
#include "continuum/base.keymap"
```

Example for 36-key Corne:

```c
#define CONFIG_WIRELESS
#include "continuum/matrix/36.h"
#include "continuum/base.keymap"
```

Use `eyelash_corne36.h` or `eyelash_corne42.h` when your PCB includes the extra encoder/joystick key positions defined in those headers.

### Build Targets

Corne targets are active in the repository CI matrix (`build.yaml`).

Current pattern:

```yaml
include:
  - board: nice_nano//zmk
    shield: corne_left nice_view_adapter nice_view
    snippet: common-config studio-rpc-usb-uart
    artifact-name: corne_left

  - board: nice_nano//zmk
    shield: corne_right nice_view_adapter nice_view
    artifact-name: corne_right

  - board: nice_nano//zmk
    shield: corne_left nice_view_adapter nice_view
    cmake-args: -DCONFIG_ZMK_SPLIT_ROLE_CENTRAL=n
    artifact-name: corne_left_w_dongle

  - board: nice_nano//zmk
    shield: corne_dongle
    snippet: studio-rpc-usb-uart
    artifact-name: corne_dongle

  - board: nice_nano//zmk
    shield: corne_dongle zdd_adapter dongle_display
    snippet: studio-rpc-usb-uart
    artifact-name: corne_zdd_dongle

  - board: xiao_ble//zmk
    shield: corne_dongle prospector_adapter
    snippet: studio-rpc-usb-uart prospector-config
    cmake-args: -DCONFIG_ZMK_KEYBOARD_NAME=\"Corne\ PRSP\"
    artifact-name: corne_prospector_dongle

  - board: eyelash_corne_left
    shield: nice_view
    snippet: common-config studio-rpc-usb-uart
    artifact-name: eyelash_corne_left

  - board: eyelash_corne_right
    shield: nice_view
    artifact-name: eyelash_corne_right

  - board: eyelash_corne_left
    shield: nice_view
    cmake-args: -DCONFIG_ZMK_SPLIT_ROLE_CENTRAL=n
    artifact-name: eyelash_corne_left_w_dongle

  - board: nice_nano//zmk
    shield: eyelash_corne_dongle zdd_adapter dongle_display
    snippet: studio-rpc-usb-uart
    cmake-args: -DCONFIG_ZMK_KEYBOARD_NAME=\"EyelashCorneZDD\"
    artifact-name: eyelash_corne_zdd_dongle

  - board: xiao_ble//zmk
    shield: eyelash_corne_dongle prospector_adapter
    snippet: studio-rpc-usb-uart prospector-config
    cmake-args: -DCONFIG_ZMK_KEYBOARD_NAME=\"ELCornePRSP\"
    artifact-name: eyelash_corne_prospector_dongle
```

### Flashing

1. Build or download `corne_left.uf2` and `corne_right.uf2`.
2. Connect left half via USB.
3. Enter bootloader mode (usually double-tap reset).
4. Copy `corne_left.uf2` to the mounted drive.
5. Repeat for right half with `corne_right.uf2`.
6. Optional: flash shared reset artifacts (`reset_nice_nano_zmk` or `reset_xiao_ble_zmk`) to clear stale bonds/settings.

## Status

- Matrix support exists in Continuum headers.
- Dedicated `config/corne.keymap` and `config/corne.conf` are committed.
- Corne build targets are enabled in `build.yaml`:
  - `corne_left`, `corne_right`, `corne_left_w_dongle`
  - `corne_dongle`, `corne_zdd_dongle`, `corne_prospector_dongle`
  - `eyelash_corne_left`, `eyelash_corne_right`, `eyelash_corne_left_w_dongle`
  - `eyelash_corne_zdd_dongle`, `eyelash_corne_prospector_dongle`
  - Shared reset artifacts: `reset_nice_nano_zmk`, `reset_xiao_ble_zmk`
