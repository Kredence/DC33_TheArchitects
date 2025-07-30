# IP Badge (Work in Progress)

This repository contains firmware for a custom RP2040-Zero badge designed for conferences and interactive events. It features a 286x78 ST7789P3 display, 83 WS2812B LEDs, external W25Q flash, and APS6406L PSRAM. The firmware is written in MicroPython with modular support for display and lighting patterns because I yearn for pain.

---

## Status

**This project is currently under active development.**  
Expect incomplete features, changing configurations, and all that. Contributions and testing are welcome.

Please be kind, this is my first swing at as project of this size :)

---

## Flashing the RP2040-Zero with MicroPython

1. **Download Firmware**
   - Go to: https://micropython.org/download/rp2-pico/
   - Download the `.uf2` file for the **Raspberry Pi Pico** (RP2040).

2. **Enter Boot Mode**
   - Hold the `BOOTSEL` button on the RP2040-Zero.
   - Plug the badge into your computer via USB.
   - Release the button once connected.
   - A new USB mass storage drive named `RPI-RP2` should appear.

3. **Flash MicroPython**
   - Drag and drop the `.uf2` file onto the `RPI-RP2` drive.
   - The board will reboot automatically into MicroPython.

---

## Uploading Firmware to the Badge

You can upload all firmware files from the `/Dev` folder using either:

### Option A: Visual Studio Code with MicroPico

1. Install VSCode
2. Install the **MicroPico** extension in VSCode.
   <img width="482" height="250" alt="image" src="https://github.com/user-attachments/assets/7f62ee23-511c-4545-8fb1-d48c4edb95df" />
3. Open the `/Dev` project folder **if you upload the whole IP/Dev folder, the badge won't boot**
4. Select `Initialize MicroPico Project` from the MicroPico menu (CTRL+Shift+P to open the command palette)
3. Use the “Upload All Files” or “Sync Folder” command to copy the contents of `Dev/` to the badge.

### Option B: Thonny IDE

1. Open Thonny and configure the interpreter:
   - `Tools → Options → Interpreter → MicroPython (Raspberry Pi Pico) COMX`
2. Open the `Dev/` folder in Thonny.
3. Select all files and upload them to the board:
   - Right-click → `Upload to /`

> After uploading, **restart the badge** by unplugging and replugging the USB cable or pressing the reset button.

---

## Configuration Settings

Key settings are stored in `config.py` and `settings.json`:

| Setting | Description |
|--------|-------------|
| `BL_BRIGHTNESS` | Display backlight brightness (PWM duty, 0–65535) |
| `THEME_FONT` | Font color palette name (used for handle display) |
| `THEME_COLOR` | RGB tuple used as default LED color |
| `THEME_PALETTE_NAME` | Name of LED color palette (maps to `fonts/palettes.py`) |
| `BRIGHTNESS` | Global LED brightness scaling (float 0.0–1.0) |
| `DEFAULT_HANDLE` | Fallback handle if none is set |
| `SETTINGS_FILE` | JSON file storing users handle and nothing more. *It only exists when the menu.py runs* |

---

## Project Layout
```
Dev/
├── boot.py # Flash boot setup and filesystem mount
├── main.py # Main runtime loop (display + lighting)
├── config.py # Central configuration for pins, colors, brightness
├── settings.json # Stores user-defined settings
├── /lib # Custom libraries (display, flash, filesystem)
├── /fonts # Bitmap fonts and color palettes
├── /patterns # Lighting and display patterns
└── /external # External assets (e.g. BMP frames for animations)
```
---

## Additional Notes

- Display and lighting effects are asynchronous and can run in parallel as long as asyncio is used
- Custom lighting patterns and glitch text animations are located in `/patterns`.
- External flash is formatted using FAT and mounted at boot. If you can help with reformatting to LittleFS, I'd take the help.
- Working on additional fonts:
    - Fonts are VGA-style bitmaps loaded from `/fonts`.
- Working on getting GIFs functional or at least some different display patterns

---

## LED Pattern Function Examples

Below are examples of lighting functions available in `/patterns`. Each pattern supports brightness scaling and color palettes.

### `twinkle(section="sky", count=4, delay=0.1)`

Lights up random LEDs in a specified section with a gentle fade-in and fade-out effect. Multiple LEDs can twinkle at the same time.

- **Parameters**:
  - `section`: LED group to animate (e.g. `"sky"`, `"beam"`)
  - `count`: How many LEDs to animate simultaneously
  - `delay`: Time between twinkles

### `chase(section="bottom", count=2, bounce=True)`

Animates a “chase” light that moves left-to-right (and optionally right-to-left). Ideal for creating sweeping effects across segments.

- **Parameters**:
  - `section`: LED group to animate
  - `count`: How many LEDs are lit at once
  - `bounce`: If `True`, animation reverses direction at the end

### `breathe(section="all_leds", cycles=3, min_brightness=0.1, max_brightness=0.7)`

Smoothly fades all LEDs in and out in a breathing rhythm.

- **Parameters**:
  - `section`: LED group to animate
  - `cycles`: Number of fade-in/out loops
  - `min_brightness`: Lowest brightness point
  - `max_brightness`: Highest brightness point

### `glitch_flash(section="left_glitch", use_theme_color=True)`

Creates a static-like flashing glitch effect using either the theme color or randomized values.

- **Parameters**:
  - `section`: LED group to animate
  - `use_theme_color`: If `True`, use the theme color instead of random
