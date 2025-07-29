import uasyncio as asyncio
import urandom
import neopixel
import random
from machine import Pin

from config import LED_PIN, LED_COUNT, BRIGHTNESS, THEME_PALETTE_NAME
from fonts.palettes import PALETTES
from patterns import led_map

np = neopixel.NeoPixel(Pin(LED_PIN), LED_COUNT)
THEME_PALETTE = PALETTES[THEME_PALETTE_NAME]

def set_pixel(i, color, brightness=1.0):
    r, g, b = color
    np[i] = (int(r * brightness), int(g * brightness), int(b * brightness))

async def fade_pixel(i, color, steps=5, speed=0.03):
    for level in range(steps + 1):
        set_pixel(i, color, brightness=(level / steps) * BRIGHTNESS)
        np.write()
        await asyncio.sleep(speed)
    for level in reversed(range(steps + 1)):
        set_pixel(i, color, brightness=(level / steps) * BRIGHTNESS)
        np.write()
        await asyncio.sleep(speed)

async def twinkle(
    count=30,
    speed=0.03,
    simultaneous=1,
    section="all_leds",
    randomize_speed=False,
    color_ramp=False,
):
    led_group = getattr(led_map, section, led_map.all_leds)
    ramp_index = 0

    for _ in range(count // simultaneous):
        tasks = []
        for _ in range(simultaneous):
            i = random.choice(led_group)

            if color_ramp:
                color = THEME_PALETTE[ramp_index % len(THEME_PALETTE)]
                ramp_index += 1
            else:
                color = random.choice(THEME_PALETTE)

            spd = speed
            if randomize_speed:
                spd += urandom.getrandbits(4) * 0.002  # adds 0–0.03s

            tasks.append(fade_pixel(i, color, speed=spd))
        await asyncio.gather(*tasks)

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

# test
if __name__ == "__main__":
    asyncio.run(twinkle(
        count=60,
        speed=0.03,
        simultaneous=3,
        section="sky",
        randomize_speed=True,
        color_ramp=True
    ))
