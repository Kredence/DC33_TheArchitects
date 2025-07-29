from time import sleep
import neopixel
import random
import urandom
import uasyncio as asyncio
from machine import Pin
from config import LED_PIN, LED_COUNT, BRIGHTNESS, THEME_COLOR

# Settong a theme color - like goldish-yellow
# THEME_COLOR = (255, 251, 0)

# Create NeoPixel object
np = neopixel.NeoPixel(Pin(LED_PIN), LED_COUNT)
# np.brightness = BRIGHTNESS  # Only supported in Adafruit CircuitPython, not MicroPython. Adjusting brightness manually (in the config.py)

# START - helper functionzzzz
def set_pixel(i, color, brightness=BRIGHTNESS):
    r, g, b = color
    np[i] = (int(r * brightness), int(g * brightness), int(b * brightness))

def fade_pixel(i, color, steps=5, delay=0.02):
    r, g, b = color
    for level in reversed(range(steps + 1)):
        brightness = level / steps
        set_pixel(i, (r, g, b), brightness=brightness)
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

# END - helper functionzzzz

# START - lighting patterns

def glitchy_bottom_chase(delay=0.07, twinkle_count=2, randomize=False):
    start = 69
    end = min(84, LED_COUNT)
    bottom_zone = list(range(start, end))
    zone_len = len(bottom_zone)

    for _ in range(zone_len):
        used = set()

        for _ in range(twinkle_count):
            while True:
                idx = urandom.getrandbits(4) % zone_len
                if idx not in used:
                    used.add(idx)
                    break

            led = bottom_zone[idx]

            color = (
                (urandom.getrandbits(8), urandom.getrandbits(8), urandom.getrandbits(8))
                if randomize else THEME_COLOR
            )

            set_pixel(led, color)

        np.write()
        sleep(delay)

        for idx in used:
            fade_pixel(bottom_zone[idx], color)

def bottom_chase(color=(255, 251, 0), delay=0.07, active_count=1.5):
    start = 67
    end = min(82, LED_COUNT)  # safely cap to avoid out-of-range

    active = []

    for i in range(start, end):
        set_pixel(i, color)
        active.append(i)

        if len(active) > active_count:
            idx_to_fade = active.pop(0)
            fade_pixel(idx_to_fade, color)

        np.write()
        sleep(delay)

    for i in active:
        fade_pixel(i, color)

def run():
    bottom_chase()

run()