# Development TODO

Use this as a process tracker.

Rule of done for each firmware target:

- [ ] target implemented (shield/config/keymap/overlay)
- [ ] target added to `build.yaml`
- [ ] CI build passed
- [ ] runtime test passed (pairing/reconnect/role behavior)
- [ ] docs updated

## 1. Dongle

### 1.0 Naming / baseline

- [x] Freeze naming convention
  - [x] Single: `<keyboard>_<hardware>_<role>` : This allows to build with wildcard for single keyboard
  - [x] central/scanner: `<hardware>_<role>`
- [x] Freeze hardware IDs (`zdd`, `prospector`)
- [x] Freeze role names (`dongle`, `central`, `scanner`)

### ZMK Dongle Display(`zdd`)

- [ ] implement device single
  - [ ] totem
  - [ ] urchin
  - [ ] sofle
  - [ ] eyelash sofle
  - [ ] cornix
  - [ ] delta omega
  - [ ] corne
  - [ ] eyelash corne variation
- [ ] develop central
  - [ ] totem
  - [ ] urchin
  - [ ] sofle
  - [ ] eyelash sofle
  - [ ] cornix
  - [ ] delta omega
  - [ ] corne
- [ ] develop scanner
  - [ ] totem
  - [ ] urchin
  - [ ] sofle
  - [ ] eyelash sofle
  - [ ] cornix
  - [ ] delta omega
  - [ ] corne

### Prospector hardware(`prospector`) + YADS firmware

- [ ] implement device single
  - [ ] totem
  - [ ] urchin
  - [ ] sofle
  - [ ] eyelash sofle
  - [ ] cornix
  - [ ] delta omega
  - [ ] corne
- [ ] develop central
  - [ ] totem
  - [ ] urchin
  - [ ] sofle
  - [ ] eyelash sofle
  - [ ] cornix
  - [ ] delta omega
  - [ ] corne
- [ ] develop scanner
  - [ ] totem
  - [ ] urchin
  - [ ] sofle
  - [ ] eyelash sofle
  - [ ] cornix
  - [ ] delta omega
  - [ ] corne

## 2. Keyboard / Devices

- [x] Totem: verify left/right/reset targets
- [x] Urchin: verify left/right/reset targets
- [x] Sofle: verify left/right/reset targets
- [x] Corne: verify target status and doc status
- [ ] Cornix: verify target status and doc status
- [x] Delta Omega: verify target status and doc status

- [ ] `*_left_w_dongle` targets: verify display config is correct for each keyboard
- [x] Continuum integration: remove duplicated per-keyboard keymap logic
- [x] Verify sleep/battery/BLE defaults per keyboard family
- [ ] Verify split peripheral counts are correct for each central role target

## 3. Documentation

- [x] Keep `README.md` and `README_KO.md` synchronized after each feature batch
- [x] Keep dongle role wording consistent (`dongle`, `central`, `scanner`)
- [x] Update `docs/dongle.md` matrix and examples after each new target
- [x] Run docs sanity pass against `docs/docs_rules.md` (used as baseline template, expanded where needed)
- [x] Keep `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, and docs rules aligned
- [ ] Ensure each keyboard doc has current build/flash/troubleshooting sections

## 4. CICD

- [x] Ensure each target has unique `artifact-name`
- [x] Add selective build process
- [x] Add local developement support with docker + cmake command
- [x] Release workflow: attach firmware assets (`.uf2/.bin/.hex`) with checksums
- [x] Release docs: clarify GitHub source archives are always auto-generated

## 5. Nice to Have

- [ ] Add standalone compatibility matrix doc (`keyboard x hardware x role`)
- [ ] Add changelog template focused on firmware behavior changes
- [ ] Add simple architecture diagrams for each dongle role
- [x] Deep sleep rollout (`CONFIG_ZMK_SLEEP`, `CONFIG_ZMK_IDLE_SLEEP_TIMEOUT`) and per-keyboard wakeup-source validation
- [x] Soft-off UX (`CONFIG_ZMK_PM_SOFT_OFF`, `&soft_off`) with hold-time and wake strategy per board
- [x] External power gating for display/lighting builds (`CONFIG_ZMK_EXT_POWER`, `zmk,ext-power-generic`)
- [x] Split battery reporting pilot (`CONFIG_ZMK_SPLIT_BLE_CENTRAL_BATTERY_LEVEL_PROXY` + `...FETCHING`)
- [x] BLE stability/security pilot (`CONFIG_ZMK_BLE_EXPERIMENTAL_CONN`, passkey entry) with re-pair test plan
- [x] Studio locking policy tuning (`CONFIG_ZMK_STUDIO_LOCKING`, idle lock timeout) and recovery SOP
- [x] Display power/perf tuning baseline (`CONFIG_ZMK_DISPLAY_BLANK_ON_IDLE`, tick period) per display target
- [x] Bluetooth profile ops hardening (`BT_SEL/BT_DISC/BT_CLR_ALL`) and user-facing keymap conventions
- [x] Pointing device pilot for select boards (`CONFIG_ZMK_POINTING`) with host re-pair validation
