# # /patterns/breathe.py

# import uasyncio as asyncio
# import neopixel
# from machine import Pin
# from config import LED_PIN, LED_COUNT, BRIGHTNESS, THEME_COLOR

# np = neopixel.NeoPixel(Pin(LED_PIN), LED_COUNT)

# def set_pixel(i, color, brightness=BRIGHTNESS):
#     r, g, b = color
#     np[i] = (int(r * brightness), int(g * brightness), int(b * brightness))

# def fade_out():
#     for i in range(LED_COUNT):
#         np[i] = (0, 0, 0)
#     np.write()

# async def breathe(cycles=3, delay=0.02):
#     for _ in range(cycles):
#         for b in range(0, 100, 3):
#             for i in range(LED_COUNT):
#                 set_pixel(i, THEME_COLOR, brightness=b / 100)
#             np.write()
#             await asyncio.sleep(delay)
#         for b in range(100, -1, -3):
#             for i in range(LED_COUNT):
#                 set_pixel(i, THEME_COLOR, brightness=b / 100)
#             np.write()
#             await asyncio.sleep(delay)
#     fade_out()

# # test
# if __name__ == "__main__":
#     asyncio.run(breathe())

import uasyncio as asyncio
import neopixel
import random
import urandom
import math
from machine import Pin

from config import LED_PIN, LED_COUNT, BRIGHTNESS, THEME_PALETTE_NAME
from fonts.palettes import PALETTES
from patterns import led_map

np = neopixel.NeoPixel(Pin(LED_PIN), LED_COUNT)
THEME_PALETTE = PALETTES[THEME_PALETTE_NAME]

def set_pixel(i, color, brightness=1.0):
    r, g, b = color
    np[i] = (int(r * brightness), int(g * brightness), int(b * brightness))

def eased(level, easing="linear"):
    t = level / 100
    if easing == "sine":
        return math.sin(t * math.pi / 2)
    return t  # linear fallback

async def breathe(
    section="all_leds",
    loop_count=3,
    simultaneous=4,
    color_ramp=False,
    randomize_speed=False,
    fade_out=True,
    min_brightness=0.1,
    max_brightness=0.7,
    easing="sine"  # "linear" or "sine"
):
    led_group = getattr(led_map, section, led_map.all_leds)
    ramp_index = 0

    def get_next_color():
        nonlocal ramp_index
        if color_ramp:
            color = THEME_PALETTE[ramp_index % len(THEME_PALETTE)]
            ramp_index += 1
        else:
            color = random.choice(THEME_PALETTE)
        return color

    for _ in range(loop_count):
        # Fade in
        for level in range(0, 101, 4):
            current_brightness = min_brightness + eased(level, easing) * (max_brightness - min_brightness)
            for _ in range(simultaneous):
                i = random.choice(led_group)
                color = get_next_color()
                set_pixel(i, color, brightness=current_brightness)
            np.write()
            delay = 0.02
            if randomize_speed:
                delay += urandom.getrandbits(3) * 0.002
            await asyncio.sleep(delay)

        # Fade out
        for level in reversed(range(0, 101, 4)):
            current_brightness = min_brightness + eased(level, easing) * (max_brightness - min_brightness)
            for _ in range(simultaneous):
                i = random.choice(led_group)
                color = get_next_color()
                set_pixel(i, color, brightness=current_brightness)
            np.write()
            delay = 0.02
            if randomize_speed:
                delay += urandom.getrandbits(3) * 0.002
            await asyncio.sleep(delay)

    if fade_out:
        await final_fade_out()

async def final_fade_out():
    steps = 5
    for level in reversed(range(steps + 1)):
        for i in range(LED_COUNT):
            r, g, b = np[i]
            np[i] = (
                int(r * level / steps),
                int(g * level / steps),
                int(b * level / steps)
            )
        np.write()
        await asyncio.sleep(0.02)
    np.fill((0, 0, 0))
    np.write()

# # test
if __name__ == "__main__":
    asyncio.run(breathe(
        section="all",
        loop_count=1,
        simultaneous=5,
        color_ramp=True,
        randomize_speed=True,
        min_brightness=0.1,
        max_brightness=0.65,
        easing="sine",
        fade_out=True
    ))
