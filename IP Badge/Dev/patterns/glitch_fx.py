from time import sleep
import neopixel
import random
import urandom
import uasyncio as asyncio
from machine import Pin
from config import LED_PIN, LED_COUNT, BRIGHTNESS,THEME_PALETTE_NAME

# Setting a theme color
THEME_COLOR = THEME_PALETTE_NAME

# Create NeoPixel object
np = neopixel.NeoPixel(Pin(LED_PIN), LED_COUNT)

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
# not sure I'll use this one
# def glitch_twinkle(
#     flashes=20,
#     delay=0.02,
#     randomize=False,
#     twinkle_count=3,
#     linger_chance=0.1,
#     theme_color=(255, 251, 0)
# ):
#     left_glitch = list(range(0, 8))
#     right_glitch = list(range(61, 69))
#     glitch_zone = left_glitch + right_glitch
#     glitch_len = len(glitch_zone)

#     for _ in range(flashes):
#         used = set()

#         for _ in range(twinkle_count):
#             # Pick a unique random LED index
#             while True:
#                 idx = urandom.getrandbits(4) % glitch_len
#                 if idx not in used:
#                     used.add(idx)
#                     break

#             led = glitch_zone[idx]

#             # Pick color
#             if randomize:
#                 c = (
#                     urandom.getrandbits(8),
#                     urandom.getrandbits(8),
#                     urandom.getrandbits(8)
#                 )
#             else:
#                 c = theme_color

#             set_pixel(led, c)

#         np.write()
#         sleep(delay)

#         for idx in used:
#             led = glitch_zone[idx]
#             # Linger chance (~0–255)
#             linger_test = urandom.getrandbits(8)
#             if linger_test > int(linger_chance * 255):
#                 fade_pixel(led, c)
#             else:
#                 sleep(delay * 3)
#                 fade_pixel(led, c)

# Keeps the edges looping in a twinkle - thinking like a night sky
# def glitch_twinkle_loop(
#     delay=0.1,
#     randomize=False,
#     twinkle_count=3,
#     linger_chance=0.1,
#     fade_steps=5,
#     fade_delay=0.08
# ):
#     left_glitch = list(range(0, 7))       # 0–6
#     right_glitch = list(range(61, 68))    # 61–67
#     glitch_zone = left_glitch + right_glitch
#     glitch_len = len(glitch_zone)

#     while True:
#         used = set()

#         for _ in range(twinkle_count):
#             while True:
#                 idx = urandom.getrandbits(4) % glitch_len
#                 if idx not in used:
#                     used.add(idx)
#                     break

#             led = glitch_zone[idx]

#             color = (
#                 (
#                     urandom.getrandbits(8),
#                     urandom.getrandbits(8),
#                     urandom.getrandbits(8)
#                 ) if randomize else THEME_COLOR
#             )

#             set_pixel(led, color)

#         np.write()
#         sleep(delay)

#         for idx in used:
#             led = glitch_zone[idx]
#             linger = urandom.getrandbits(8) > int(linger_chance * 255)

#             if linger:
#                 sleep(delay * 3)

#             fade_pixel(led, color, steps=fade_steps, delay=fade_delay)

# def glitchy_triangle_wipe(delay=0.03, randomize=False):
#     triangle_zone = list(range(14, 60))
#     used = set()

#     while len(used) < len(triangle_zone):
#         idx = urandom.getrandbits(6) % len(triangle_zone)
#         if idx in used:
#             continue
#         used.add(idx)
#         i = triangle_zone[idx]

#         color = (
#             (urandom.getrandbits(8), urandom.getrandbits(8), urandom.getrandbits(8))
#             if randomize else THEME_COLOR
#         )

#         set_pixel(i, color)
#         np.write()
#         sleep(delay)
#         fade_pixel(i, color)

async def glitchy_triangle_wipe(delay=0.03, randomize=False):
    triangle_zone = list(range(14, 60))
    used = set()

    while len(used) < len(triangle_zone):
        idx = urandom.getrandbits(6) % len(triangle_zone)
        if idx in used:
            continue
        used.add(idx)
        i = triangle_zone[idx]

        color = (
            (urandom.getrandbits(8), urandom.getrandbits(8), urandom.getrandbits(8))
            if randomize else THEME_COLOR
        )

        set_pixel(i, color)
        np.write()
        await asyncio.sleep(delay)
        fade_pixel(i, color)

async def glitchy_bottom_chase(delay=0.07, twinkle_count=3, randomize=False):
    bottom_zone = list(range(69, min(84, LED_COUNT)))
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
        await asyncio.sleep(delay)

        for idx in used:
            fade_pixel(bottom_zone[idx], color)

# def bottom_chase(color=(255, 251, 0), delay=0.07, active_count=1.5):
#     start = 69
#     end = min(84, LED_COUNT)  # safely cap to avoid out-of-range

#     active = []

#     for i in range(start, end):
#         set_pixel(i, color)
#         active.append(i)

#         if len(active) > active_count:
#             idx_to_fade = active.pop(0)
#             fade_pixel(idx_to_fade, color)

#         np.write()
#         sleep(delay)

#     for i in active:
#         fade_pixel(i, color)

# def run():
    # glitch_twinkle()
#     triangle_wipe()
#     bottom_chase()
#     fade_out()

# START - Runtime examples
# glitch_twinkle_loop(randomize=False, twinkle_count=2, linger_chance=0.7) # Randomize=False will use the theme color 
# triangle_wipe()
# bottom_chase()
# glitch_twinkle_loop()
# glitch_twinkle()
# glitchy_triangle_wipe(randomize=False)  # use theme color
# glitchy_bottom_chase(twinkle_count=3, randomize=True)  # random glitch lights
# END - Runtime examples

# def glitch_sequence(
#     triangle_twinkle_delay=0.03,
#     bottom_twinkle_delay=0.07,
#     bottom_twinkle_count=3,
#     randomize=False
# ):
#     glitchy_triangle_wipe(
#         delay=triangle_twinkle_delay,
#         randomize=randomize
#     )

#     glitchy_bottom_chase(
#         delay=bottom_twinkle_delay,
#         twinkle_count=bottom_twinkle_count,
#         randomize=randomize
#     )

# Theme color glitch sequence
# glitch_sequence(randomize=False)

# Or a colorful random glitch sequence
# glitch_sequence(randomize=True, bottom_twinkle_count=4)


async def glitch_sequence_run_once(randomize=False):
    await asyncio.gather(
        glitchy_triangle_wipe(delay=0.02, randomize=randomize),
        glitchy_bottom_chase(delay=0.05, twinkle_count=3, randomize=randomize)
    )

# asyncio.run(glitch_sequence_run_once(randomize=False)) # Randomize = False will use THEME_COLOR

async def glitch_idle_loop(randomize=False):
    while True:
        await glitch_sequence_run_once(randomize=randomize)
        await asyncio.sleep(0.2)

# asyncio.run(glitch_idle_loop(randomize=True)) # Randomize = False will use THEME_COLOR

def run():
    asyncio.run(glitch_idle_loop(randomize=True))