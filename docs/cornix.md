# Cornix

![Cornix thumbnail](/docs/images/cornix_thumbnail.webp)

This document covers the Cornix integration used in this repository.

## Reference Material

- Cornix project and docs: <https://cornixhub.com/>
- Cornix ZMK module source: <https://github.com/hitsmaxft/zmk-keyboard-cornix>
- ZMK docs: <https://zmk.dev/docs>

## Hardware Overview

- 48-key column-staggered split keyboard
- Wireless split operation via dedicated left/right boards
- Optional RGB indicator shield is available via `cornix_indicator`

## Layout

### Physical Layout

![Cornix layout](/docs/images/cornix_layout.svg)

### Keymap

![Cornix keymap](/docs/images/cornix_keymap.svg)

## Support Snapshot

| Target | Board | Shield | Snippet | Artifact Name | Status |
| --- | --- | --- | --- | --- | --- |
| Left half | `cornix_left` | none | `common-config studio-rpc-usb-uart` | `cornix_left` | Active |
| Right half | `cornix_right` | none | none | `cornix_right` | Active |
| Reset | `cornix_right` | `settings_reset` | none | `cornix_reset` | Active |
| Left half (dongle split) | `cornix_left` | none | none | `cornix_left_w_dongle` | Active |
| Dongle (ZDD) | `nice_nano_v2` | `cornix_dongle zdd_adapter dongle_display` | `studio-rpc-usb-uart` | `cornix_zdd_dongle` | Active |
| Dongle reset | `nice_nano_v2` | `settings_reset` | none | `cornix_zdd_dongle_reset` | Active |

## Warning: device breakdown recovery

> [!Note]
> For instructions on flashing or resetting firmware, see the [#HOW TO USE/Advanced mode](#advanced-mode) section below.
> You may need to reset the firmware before flashing new firmware.

### Flashing/Resetting Default Firmware

The original Cornix firmware is available at [Original firmware](/docs/files/cornix_firmwareV1.11.zip).
Flash this firmware to the keyboard halves to update/recover the Cornix keyboard.

### Bootloader Recovery

- The original RMK firmware removes the SoftDevice. So, before flashing new ZMK firmware, you need to restore the SoftDevice first.

#### Extracting SoftDevice (s140) for nRF52840

Download the bootloader for nRF52840 from:

- Official repository: <https://github.com/joric/nrfmicro/wiki/Bootloader>
- This bootloader is compatible with nRF52840-based keyboards using ZMK firmware

These commands extract the SoftDevice (s140) from the bootloader HEX file and convert it to UF2 format for flashing:

```bash
# Convert HEX to binary
arm-none-eabi-objcopy -I ihex -O binary pca10056_bootloader-0.2.11_s140_6.1.1.hex full_flash.bin

# Extract SoftDevice section
# Skip bootloader (4096 bytes, start address 0x1000)
# Count matches SoftDevice size (151016 bytes, end address: 0x25DE7 )
dd if=full_flash.bin of=s140_sd_only.bin bs=1 skip=4096 count=151016

# method 1: generate hex file,  flashing with nrfutil or nrf connect
arm-none-eabi-objcopy -O ihex -I binary s140_sd_only.bin s140_sd_only.hex
arm-none-eabi-objcopy --change-address 0x1000 s140_sd_only.hex  s140_sd_only.hex

# method 2: generate uf2 , flash by uf2 bootloader
# Convert bin content to UF2 format with start address for flashing
python3 uf2conv.py s140_sd_only.bin -f 0xada52840 -b 0x1000 -c -o s140_restore.uf2
```

nRF Connect for Desktop's Programmer is very useful for getting the SD address and size from the bootloader HEX file.

<img width="736" height="691" alt="图片" src="https://github.com/user-attachments/assets/be124646-870a-48d6-9387-d7cb043f4848" />

#### Extracting SoftDevice (s130) for nRF51

Command to extract SoftDevice (s130) section:

```bash
# Skip bootloader (4096 bytes)
dd if=full_flash.bin of=s132_sd_only.bin bs=1 skip=4096 count=155648
```

## How to Use

### Easy mode

> [!Note]
> Key remapping in wireless mode may fail due to signal interference. If connection fails, please retry or switch to wired mode. Key remapping works in both wired and wireless modes.

1. Connect the Cornix to the PC.
2. Open the key remapping website: [Vial](https://vial.rocks)
3. Click “Start Vial” in the center of the screen, then select “Cornix” (wired mode) or “Unknown Device (0000:0000)” (wireless mode) in the pop-up window at the top left.
4. After successful connection, enter the driver page to customize key functions

### Advanced mode

#### Reuse the config repo

1. Fork or clone this repo
   - It is recommended to fork this repo to keep your config changes.
2. Edit keymap
   - You can edit it directly or use the [ZMK Keymap Editor](https://nickcoutsos.github.io/keymap-editor/)
3. Build with github actions
   - After pushing, GitHub Actions will automatically run the build to generate new firmware.
4. Flash your keyboard
   - connect cornix with pc with wire.
   - double-tapping the reset button to enter bootloader mode.
   - Drag'n'drop the `.uf2` file onto the mounted drive.

#### Build Firmware

Use your preferred method to build

1. Create new repo based on [ZMK config template](https://github.com/zmkfirmware/unified-zmk-config-template):
   - use this template -> create new repository
2. Clone the repo:

   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   cd YOUR_REPO_NAME
   ```

3. Initialize ZMK development environment:

   ```bash
   west init -l config/
   west update
   west zephyr-export
   ```

   > [!Note]
   > You should thoroughly read the ZMK documentation before proceeding, as ZMK firmware development has a learning curve.
   >
   > - ZMK Customization Guide: <https://zmk.dev/docs/customization>
   > - ZMK Configuration: <https://zmk.dev/docs/user-setup>

4. Add Cornix shield

#### How to add Cornix shield

1. Modify west.yml
   - Edit the `config/west.yml` file, add to the `manifest/remotes` section:

   ```yaml
   remotes:
     - name: zmkfirmware
       url-base: https://github.com/zmkfirmware
     - name: cornix-shield
       url-base: https://github.com/hitsmaxft
     - name: urob
       url-base: https://github.com/urob
   ```

   - Add to the `manifest/projects` section:

   ```yaml
   projects:
     - name: zmk
       remote: zmkfirmware
       import: app/west.yml
     - name: zmk-keyboard-cornix
       remote: cornix-shield
     - name: zmk-helpers
       remote: urob
   ```

2. Update Dependencies

   ```bash
   west update
   ```

3. Configure Build
   - Edit the `build.yaml` file, add:

   > [!NOTE]
   >
   > 1. Use `cornix_left`, `cornix_right`, and `cornix_reset` for direct split mode.
   > 2. Use `cornix_left_w_dongle`, `cornix_zdd_dongle`, and `cornix_zdd_dongle_reset` for dongle mode.
   > 3. Add `cornix_indicator` shield to enable RGB LED (higher power use).

   ```yaml
   include:
     - board: cornix_left
       # shield: cornix_indicator
       snippet: common-config studio-rpc-usb-uart
       artifact-name: cornix_left

     - board: cornix_right
       # shield: cornix_indicator
       artifact-name: cornix_right

     - board: cornix_right
       shield: settings_reset
       artifact-name: cornix_reset

     - board: cornix_left
       cmake-args: -DCONFIG_ZMK_SPLIT_ROLE_CENTRAL=n
       artifact-name: cornix_left_w_dongle

     - board: nice_nano_v2
       shield: cornix_dongle zdd_adapter dongle_display
       snippet: studio-rpc-usb-uart
       artifact-name: cornix_zdd_dongle

     - board: nice_nano_v2
       shield: settings_reset
       artifact-name: cornix_zdd_dongle_reset
   ```

4. Build Firmware

   Use your preferred method to build
   - No need to recover the SD since 2.3.
   - Flash reset.uf2 to both sides of Cornix.
   - Flash left and right .uf2 files.
   - Reset both sides at the same time.

5. Flash Firmware

   Flash the generated `.uf2` files to the corresponding microcontroller:
   - Left half: `build/left/zephyr/zmk.uf2`
   - Right half: `build/right/zephyr/zmk.uf2`
