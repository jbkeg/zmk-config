# Known Build Issues (Non-Blocking)

This document tracks warning-level issues that do not currently block firmware generation for this repository.

## Verification Snapshot

- Date: 2026-02-28
- Build command set:
  - `docker compose run --rm zmk-build-stable --skip-update --jobs 8 --artifact-names <studio-targets>`
  - `docker compose run --rm zmk-build-stable --skip-update --jobs 8 --artifact-names <non-studio-targets>`
- Logs:
  - `.build/studio_targets.log`
  - `.build/non_studio_targets.log`
- Result:
  - Build status: success (`Build complete.` in both logs)
  - Artifacts: `47/47` expected UF2 outputs present in `firmware/`

## Current Warning Classes

### KI-001: Deprecated Symbol Warning

- Signature: `Deprecated symbol NRF_STORE_REBOOT_TYPE_GPREGRET is enabled.`
- Scope: Upstream Zephyr/ZMK symbol lifecycle.
- Status: Non-blocking.
- Notes: Repeats across many targets; no build failure impact.

### KI-002: USB Dependency Warning on Some Split Peripheral Builds

- Signature: `ZMK_USB ... assigned the value 'y' but got the value 'n'`
- Scope: Split role/dependency interaction (repo configuration plus upstream dependency rules).
- Status: Non-blocking.
- Notes: Seen in non-studio target builds for some split/peripheral configurations.

### KI-003: Split Role Choice Warning

- Signature: `ZMK_SPLIT_ROLE_CENTRAL ... was assigned ... but got ...`
- Scope: Configuration choice/dependency interaction.
- Status: Non-blocking.
- Notes: Seen in non-studio target builds.

### KI-004: Display Choice Warning

- Signature: `The choice symbol ZMK_DISPLAY_STATUS_SCREEN_CUSTOM ... no symbol ended up as the choice selection`
- Scope: Display shield/module choice resolution.
- Status: Non-blocking.
- Notes: Seen in studio target builds; UF2 output still generated.

### KI-005: Upstream Compile-Time Array/Bounds Warnings

- Common signatures:
  - `excess elements in array initializer`
  - `array subscript ... is outside array bounds ...`
- Scope: Upstream ZMK/app compile diagnostics.
- Status: Non-blocking.
- Notes: High-frequency warnings in generated/expanded keymap-related compile units.

### KI-006: Prospector Module Compile Warnings

- Common signatures:
  - `implicit declaration of function 'peripheral_slot_index_for_conn'`
  - `unused variable 'err'`
- Scope: External module (`prospector-zmk-module`) source.
- Status: Non-blocking.
- Notes: Does not fail link or artifact creation.

### KI-007: SSD1306 Unused Static Function Warnings

- Common signatures:
  - `'ssd1306_driver_api' defined but not used`
  - `'ssd1306_init' defined but not used`
- Scope: Upstream driver/module compile diagnostics.
- Status: Non-blocking.

## Handling Policy

- These items are currently accepted as long as:
  - firmware artifacts are produced, and
  - there are no `Build failed for ...` or `FATAL ERROR` events.
- Revisit immediately if any warning category starts causing build failure.
