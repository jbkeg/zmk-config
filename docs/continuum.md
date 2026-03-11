# Continuum

This document describes Continuum, the personal keymap framework used in this repository.

Continuum lives under `config/continuum/` and is designed to adapt one personal layout/behavior model to any keyboard I personally use. It provides reusable layers, behaviors, combos, leader sequences, and matrix mappings so different keyboards can keep one consistent typing experience.

## Purpose

Continuum exists to:

- Reuse one key behavior model across multiple keyboard sizes and physical matrices
- Minimize per-keyboard duplication in user keymaps
- Keep firmware customization focused on matrix adaptation, not rewriting layers
- Preserve consistent muscle memory across board changes

## Inspiration

Continuum is primarily inspired by:

- Miryoku layout concepts for layer structure and compact keyboard workflows
- Urob's Timeless HRM approach for reliable home-row modifier behavior

## Reference Material

- ZMK docs: <https://zmk.dev/docs>
- Miryoku: <https://github.com/manna-harbour/miryoku_zmk>
- Urob's ZMK config: <https://github.com/urob/zmk-config>
- ZMK Helpers: <https://github.com/urob/zmk-helpers>
- ZMK Auto Layer: <https://github.com/urob/zmk-auto-layer>
- ZMK Unicode: <https://github.com/urob/zmk-unicode>
- ZMK Tri-State: <https://github.com/urob/zmk-tri-state>
- ZMK Leader Key: <https://github.com/urob/zmk-leader-key>
- ZMK Adaptive Key: <https://github.com/urob/zmk-adaptive-key>

## Framework Structure

- `config/continuum/base.keymap`
  - Shared layer stack and behavior definitions.
- `config/continuum/utils/helper.h`
  - Macro helpers for behaviors, combos, layers, unicode, and conditional layers.
- `config/continuum/combos.dtsi`
  - Horizontal and vertical combo definitions.
- `config/continuum/leader.dtsi`
  - Leader-key sequences, including unicode sequences and firmware control sequences.
- `config/continuum/mouse.dtsi`
  - Pointer speed, acceleration, and precision/warp profile handling.
- `config/continuum/shortcuts.dtsi`
  - Host-OS shortcut mapping (`MAC_OS` or default Windows/Linux style).
- `config/continuum/matrix/*.h`
  - Physical-matrix to logical-position maps for each keyboard family.
- `config/continuum/unicode-chars/*.dtsi`
  - Locale unicode definitions used with `zmk-unicode`.

## Layer Model

`base.keymap` defines these layers:

- `BASE`, `EXTRA`, `TAP`, `TOOL`, `MOUSE`, `NAV`, `FN`, `NUM`, `SYS`, `GAME`

Key mechanics included in the framework:

- Timeless-style home-row mods with custom hold-tap tuning
- Combo system with HRM-safe tap behavior
- `MAGIC_SHIFT` behavior (repeat/caps-word/hold-shift)
- `SMART_NUM` behavior (num-word, sticky num, held num layer)
- `TOOL` layer combining editor shortcuts with symbol fallback
- Default 34-key thumbs: `Space/Nav`, `Enter/Fn`, `NumWord/Num`, `Magic/Shift`
- Default 34-key layer holds on alpha keys: `Z/Tool`, `?/Mouse`
- Conditional layer:
  - `FN + NUM -> SYS`
- Optional wireless system controls (`CONFIG_WIRELESS`)

## Matrix Profiles

Continuum supports multiple physical layouts through header selection
`include` to use from `config/continuum/matrix/*.h` matches with your actual keyboard layout.

### Integration Pattern

Keyboard keymaps integrate Continuum by:

1. Defining optional build flags (for example `CONFIG_WIRELESS`).
2. Overriding `ZMK_BASE_LAYER(...)` when the physical layout has extra keys or custom thumb clusters.
3. Including one matrix header.
4. Including `continuum/base.keymap`.

This keeps each keyboard keymap small while preserving shared behavior logic.

Minimal pattern:

```c
#define CONFIG_WIRELESS
#include "continuum/matrix/34.h"
#include "continuum/base.keymap"
```

Customized base-layer pattern:

```c
#define CONFIG_WIRELESS
#define ZMK_BASE_LAYER(name, LT, RT, LM, RM, LB, RB, LH, RH) \
  ZMK_LAYER(name, LT RT LM RM LB RB LH RH)
#include "continuum/matrix/totem.h"
#include "continuum/base.keymap"
```

## Required Modules

Continuum depends on modules already declared in `config/west.yml`:

- `zmk-helpers`
- `zmk-auto-layer`
- `zmk-unicode`
- `zmk-tri-state`
- `zmk-leader-key`
- `zmk-adaptive-key`

If those modules are removed from west manifest, `base.keymap` features that depend on them will fail to compile.

## Notes

- `CONFIG_WIRELESS` gates BLE/output controls in the `SYS` layer.
- `MAC_OS` changes shortcut mappings in `shortcuts.dtsi`.
- `HOST_OS` affects unicode lead/trail behavior in `helper.h`.
