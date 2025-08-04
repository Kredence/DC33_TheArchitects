import uasyncio as asyncio
import random
from time import sleep
import neopixel
from machine import Pin
from config import LED_PIN, LED_COUNT, BRIGHTNESS
from fonts.palettes import PALETTES
from patterns import led_map

np = neopixel.NeoPixel(Pin(LED_PIN), LED_COUNT)

# --- Utility Functions ---
def pick_random_palette():
    palette_name = random.choice(list(PALETTES.keys()))
    return PALETTES[palette_name]

def set_pixel(i, color, brightness=BRIGHTNESS):
    r, g, b = color
    np[i] = (int(r * brightness), int(g * brightness), int(b * brightness))

def fade_pixel(i, color, steps=5, delay=0.02):
    r, g, b = color
    for level in reversed(range(steps + 1)):
        brightness = level / steps
        set_pixel(i, (r, g, b), brightness)
        np.write()
        sleep(delay)
    set_pixel(i, (0, 0, 0))
    np.write()

def fade_out(steps=50, delay=0.03):
    for b in reversed(range(steps)):
        level = b / steps
        for i in range(LED_COUNT):
            r, g, b = np[i]
            set_pixel(i, (r, g, b), brightness=level)
        np.write()
        sleep(delay)

# --- Effects ---
async def glitchy_twinkle_section(section_list, palette, delay=0.03, twinkle_count=3):
    zone_len = len(section_list)
    for _ in range(zone_len):
        used = set()
        for _ in range(twinkle_count):
            while True:
                idx = random.randrange(zone_len)
                if idx not in used:
                    used.add(idx)
                    break

        for idx in used:
            led = section_list[idx]
            color = random.choice(palette)
            set_pixel(led, color)

        np.write()
        await asyncio.sleep(delay)

        for idx in used:
            fade_pixel(section_list[idx], color)

async def glitchy_wipe_section(section_list, palette, delay=0.03):
    used = set()
    while len(used) < len(section_list):
        idx = random.randrange(len(section_list))
        if idx in used:
            continue
        used.add(idx)
        i = section_list[idx]
        color = random.choice(palette)
        set_pixel(i, color)
        np.write()
        await asyncio.sleep(delay)
        fade_pixel(i, color)

# --- Runner ---
async def glitch_sequence(section="triangle", style="wipe"):
    palette = pick_random_palette()
    led_section = getattr(led_map, section, led_map.triangle)

    if not isinstance(led_section, list):
        raise ValueError(f"Invalid section: {section}")

    if style == "wipe":
        await glitchy_wipe_section(led_section, palette)
    elif style == "twinkle":
        await glitchy_twinkle_section(led_section, palette)
    else:
        raise ValueError(f"Unknown style: {style}")

# --- Command line entry point for testing ---
if __name__ == "__main__":
    # Choose section and style: "bottom", "triangle", "sky", etc. / "twinkle" or "wipe"
    asyncio.run(glitch_sequence(section="bottom", style="wipe"))