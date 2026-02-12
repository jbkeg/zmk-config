# Firmware Changelog Template

Use this template for release notes and milestone summaries where behavior changes matter more than raw file diffs.

## Release Metadata

- Release: `<tag or milestone name>`
- Date: `<YYYY-MM-DD>`
- Scope: `<boards/shields/targets included>`
- Base branch: `<branch>`
- Compared against: `<previous tag/commit>`
- ZMK revision: `<version or commit>`

## Summary

Short statement of what changed for users.

## Firmware Behavior Changes

### Breaking or User-Action Required

- `<change>` - `<what users must do>`

### Typing and Layer Behavior

- `<layer/behavior change>`
- `<combo or hold-tap timing change>`
- `<macro or leader sequence change>`

### Input Devices (Encoder / Joystick / Pointing)

- `<binding or direction change>`
- `<sensitivity/step change>`
- `<new or removed input behavior>`

### Wireless / Split / Profiles

- `<pairing behavior change>`
- `<split role or reconnect change>`
- `<profile switching behavior change>`

### Power / Sleep / Battery

- `<idle/sleep change>`
- `<external power/display/lighting gating change>`
- `<battery reporting change>`

### Display / Lighting / Indicators

- `<OLED/Nice!View behavior change>`
- `<underglow/status LED behavior change>`

### ZMK Studio / Runtime Configuration

- `<studio support or lock policy change>`
- `<runtime remap/metadata impact>`

## Build and Target Changes

- Added targets:
  - `<artifact-name>`
- Removed targets:
  - `<artifact-name>`
- Renamed targets:
  - `<old> -> <new>`
- Build matrix updates:
  - `<build.yaml change summary>`

## Configuration Defaults Changed

- `CONFIG_<NAME>`: `<old> -> <new>` (`<impact>`)
- `CONFIG_<NAME>`: `<old> -> <new>` (`<impact>`)

## Keymap Migration Notes

- `<old behavior> -> <new behavior>`
- `<new recommended binding/macro>`
- `<optional reset/re-pair guidance>`

## Validation Evidence

### CI

- `<workflow name>`: `<pass/fail>` (`<run link or run id>`)
- `<workflow name>`: `<pass/fail>` (`<run link or run id>`)

### Local Runtime Checks

- `<board/target>`: `<result>`
- `<board/target>`: `<result>`
- Checked scenarios:
  - `<pairing/reconnect>`
  - `<sleep/wake>`
  - `<critical layer and behavior path>`

## Known Issues / Follow-ups

- `<issue and scope>`
- `<workaround if available>`

## Rollback Plan

- Revert range: `<commit/tag range>`
- Recovery steps:
  1. Flash `<reset firmware>` if needed.
  2. Flash previous known-good firmware.
  3. Re-pair devices if bonds were changed.
