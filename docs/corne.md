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
  - board: nice_nano_v2
    shield: corne_left
    snippet: common-config studio-rpc-usb-uart
    artifact-name: corne_left

  - board: nice_nano_v2
    shield: corne_right
    artifact-name: corne_right

  - board: nice_nano_v2
    shield: settings_reset
    artifact-name: corne_reset

  - board: nice_nano_v2
    shield: corne_dongle dongle_display
    snippet: common-config scanner-advertisement
    artifact-name: corne_dongle

  - board: nice_nano_v2
    shield: corne_left_w_dongle
    cmake-args: -DCONFIG_ZMK_DISPLAY=n -DCONFIG_DISPLAY=n -DCONFIG_ZMK_DISPLAY_STATUS_SCREEN_CUSTOM=n
    artifact-name: corne_left_w_dongle

  - board: nice_nano_v2
    shield: eyelash_corne_left
    snippet: common-config studio-rpc-usb-uart
    artifact-name: eyelash_corne_left

  - board: nice_nano_v2
    shield: eyelash_corne_right
    artifact-name: eyelash_corne_right

  - board: nice_nano_v2
    shield: settings_reset
    artifact-name: eyelash_corne_reset

  - board: nice_nano_v2
    shield: eyelash_corne_dongle dongle_display
    snippet: common-config scanner-advertisement
    artifact-name: eyelash_corne_dongle

  - board: nice_nano_v2
    shield: eyelash_corne_left_w_dongle
    cmake-args: -DCONFIG_ZMK_DISPLAY=n -DCONFIG_DISPLAY=n -DCONFIG_ZMK_DISPLAY_STATUS_SCREEN_CUSTOM=n
    artifact-name: eyelash_corne_left_w_dongle
```

### Flashing

1. Build or download `corne_left.uf2` and `corne_right.uf2`.
2. Connect left half via USB.
3. Enter bootloader mode (usually double-tap reset).
4. Copy `corne_left.uf2` to the mounted drive.
5. Repeat for right half with `corne_right.uf2`.
6. Optional: flash `corne_reset.uf2` first to clear stale bonds/settings.

## Status

- Matrix support exists in Continuum headers.
- Dedicated `config/corne.keymap` and `config/corne.conf` are committed.
- Corne build targets are enabled in `build.yaml`:
  - `corne_left`, `corne_right`, `corne_reset`
  - `corne_dongle`, `corne_left_w_dongle`
  - `eyelash_corne_left`, `eyelash_corne_right`, `eyelash_corne_reset`
  - `eyelash_corne_dongle`, `eyelash_corne_left_w_dongle`
