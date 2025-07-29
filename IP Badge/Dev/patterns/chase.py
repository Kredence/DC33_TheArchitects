import uasyncio as asyncio
import neopixel
import random
import urandom
from machine import Pin

from config import LED_PIN, LED_COUNT, BRIGHTNESS, THEME_PALETTE_NAME
from fonts.palettes import PALETTES
from patterns import led_map

np = neopixel.NeoPixel(Pin(LED_PIN), LED_COUNT)
THEME_PALETTE = PALETTES[THEME_PALETTE_NAME]

def set_pixel(i, color, brightness=1.0):
    r, g, b = color
    np[i] = (int(r * brightness), int(g * brightness), int(b * brightness))

async def fade_pixel(i, color, steps=5, delay=0.02):
    for level in reversed(range(steps + 1)):
        set_pixel(i, color, brightness=(level / steps) * BRIGHTNESS)
        np.write()
        await asyncio.sleep(delay)

async def chase(
    delay=0.05,
    section="all_leds",
    simultaneous=3,
    randomize_speed=False,
    color_ramp=False,
    persistent_color=True,
    direction="forward",  # "forward", "reverse", "bounce"
    loop_count=1,
    dual_head=False,
):
    base_group = getattr(led_map, section, led_map.all_leds)
    ramp_index = 0

    def get_next_color():
        nonlocal ramp_index
        if color_ramp:
            color = THEME_PALETTE[ramp_index % len(THEME_PALETTE)]
            if persistent_color:
                ramp_index += 1
        else:
            color = random.choice(THEME_PALETTE)
        return color

    def reverse_group(g):
        return list(reversed(g))

    loops = loop_count if direction == "bounce" else 1
    for loop in range(loops):
        group = base_group

        if direction == "reverse":
            group = reverse_group(group)
        elif direction == "bounce":
            group = base_group + reverse_group(base_group)

        active = []

        for idx in range(len(group)):
            if dual_head:
                i = group[idx]
                j = group[-(idx + 1)] if idx < len(group) // 2 else None

                for pos in [i, j] if j is not None else [i]:
                    color = get_next_color()
                    set_pixel(pos, color)
                    active.append((pos, color))
            else:
                i = group[idx]
                color = get_next_color()
                set_pixel(i, color)
                active.append((i, color))

            while len(active) > simultaneous:
                idx_to_fade, c = active.pop(0)
                spd = delay
                if randomize_speed:
                    spd += urandom.getrandbits(3) * 0.003
                await fade_pixel(idx_to_fade, c, delay=spd)

            np.write()

            spd = delay
            if randomize_speed:
                spd += urandom.getrandbits(3) * 0.003
            await asyncio.sleep(spd)

        # Fade out remaining trail
        for i, c in active:
            await fade_pixel(i, c)

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
    asyncio.run(chase(
        delay=0.01,
        simultaneous=4,
        section="sky",
        direction="bounce",
        loop_count=2,
        dual_head=True,
        color_ramp=True,
        randomize_speed=False
    ))
