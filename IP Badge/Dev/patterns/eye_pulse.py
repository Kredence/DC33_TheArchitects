import uasyncio as asyncio
import random
from machine import Pin
import neopixel
from config import LED_PIN, LED_COUNT, BRIGHTNESS
from fonts.palettes import PALETTES
from patterns import led_map

np = neopixel.NeoPixel(Pin(LED_PIN), LED_COUNT)

# Select a random palette
def pick_random_palette():
    name = random.choice(list(PALETTES.keys()))
    return PALETTES[name]

# Helper: Set pixel with brightness
def set_pixel(i, color, brightness=1.0):
    r, g, b = color
    np[i] = (int(r * brightness), int(g * brightness), int(b * brightness))

# Helper: Fade-in for a section
async def fade_in_section(section, color, max_brightness=BRIGHTNESS, steps=8, delay=0.02):
    for s in range(1, steps + 1):
        b = s / steps * max_brightness
        for i in section:
            set_pixel(i, color, b)
        np.write()
        await asyncio.sleep(delay)

# Helper: Eye breathing
async def eye_breathe(color=(0, 255, 0), cycles=6, steps=20, delay=0.03):
    for _ in range(cycles):
        # Fade in
        for s in range(steps):
            b = s / steps * BRIGHTNESS
            for i in led_map.eye:
                set_pixel(i, color, b)
            np.write()
            await asyncio.sleep(delay)
        # Fade out
        for s in reversed(range(steps)):
            b = s / steps * BRIGHTNESS
            for i in led_map.eye:
                set_pixel(i, color, b)
            np.write()
            await asyncio.sleep(delay)

# Helper: Full flash
async def flash_all(color, brightness=1.0, hold=0.3):
    for i in range(LED_COUNT):
        set_pixel(i, color, brightness)
    np.write()
    await asyncio.sleep(hold)

# Helper: Fade out entire strip
async def fade_out_all(steps=10, delay=0.03):
    for s in reversed(range(steps + 1)):
        level = s / steps
        for i in range(LED_COUNT):
            r, g, b = np[i]
            set_pixel(i, (r, g, b), level)
        np.write()
        await asyncio.sleep(delay)

# Main effect
async def pulse_from_eye():
    palette = pick_random_palette()
    layers = [
        led_map.eye,
        led_map.triangle_eye_ring,
        led_map.triangle_center_tip,
        led_map.triangle_left_inner + led_map.triangle_right_inner,
        led_map.triangle_left_outter + led_map.triangle_right_outter,
        led_map.triangle,
        led_map.bottom
    ]

    # Fade each layer in, keeping previous layers lit
    for layer in layers:
        color = random.choice(palette)
        await fade_in_section(layer, color)

    # Breathe red from the eye
    await eye_breathe()

    # Flash all LEDs on
    await flash_all((255, 255, 255), brightness=1.0, hold=0.2)

    # Fade out everything
    await fade_out_all()

# Test run
if __name__ == "__main__":
    asyncio.run(pulse_from_eye())
