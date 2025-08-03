import uasyncio as asyncio
import neopixel
import random, time
from machine import Pin
from config import LED_PIN, LED_COUNT, BRIGHTNESS, BL_BRIGHTNESS, SCREEN_WIDTH, SCREEN_HEIGHT
from lib.display import init_display
from fonts.palettes import PALETTES
from patterns import led_map

# Setup
np = neopixel.NeoPixel(Pin(LED_PIN), LED_COUNT)

def set_pixel(i, color, brightness=1.0):
    r, g, b = color
    np[i] = (int(r * brightness), int(g * brightness), int(b * brightness))

async def fade_leds_out(steps=5, delay=0.02):
    for step in reversed(range(steps + 1)):
        for i in range(LED_COUNT):
            r, g, b = np[i]
            np[i] = (int(r * step / steps), int(g * step / steps), int(b * step / steps))
        np.write()
        await asyncio.sleep(delay)

async def fade_display_on(target=BL_BRIGHTNESS, step=2000, delay=0.01):
    from lib.display import pwm
    for level in range(0, target + step, step):
        pwm.duty_u16(min(level, BL_BRIGHTNESS))
        await asyncio.sleep(delay)

async def fade_display_off():
    from lib.display import pwm, display
    for level in reversed(range(0, BL_BRIGHTNESS + 2000, 2000)):
        pwm.duty_u16(min(level, BL_BRIGHTNESS))
        await asyncio.sleep(0.01)
    display.fill(display.color(0, 0, 0))

async def draw_display_fill(index, total, direction, color):
    from lib.display import display

    if direction == "horizontal":
        y = int(index * SCREEN_HEIGHT / total)
        display.rect(0, y, SCREEN_WIDTH, 2, display.color(*color), fill=True)

    elif direction == "vertical":
        x = int(index * SCREEN_WIDTH / total)
        display.rect(x, 0, 2, SCREEN_HEIGHT, display.color(*color), fill=True)

    elif direction == "center-out":
        height = int(index * SCREEN_HEIGHT / (total * 2))
        y = (SCREEN_HEIGHT // 2) - height
        display.rect(0, y, SCREEN_WIDTH, height * 2, display.color(*color), fill=True)

    await asyncio.sleep(0.01)

async def screen_corruption_cleanup(palette, duration=1.5):
    from lib.display import display
    t_start = time.ticks_ms()

    while time.ticks_diff(time.ticks_ms(), t_start) < int(duration * 1000):
        for _ in range(4):
            y = random.randint(0, SCREEN_HEIGHT - 1)
            h = random.randint(1, 3)
            x = random.randint(0, SCREEN_WIDTH - 30)
            w = random.randint(20, 40)
            color = display.color(*random.choice(palette))
            display.rect(x, y, w, h, color, fill=True)
        await asyncio.sleep(0.04)

async def wave_fx_runner(
    section="all_leds",
    direction="left-to-right",
    speed=0.05,
    mirrored=False,
    theme_palette_name="IP_GOLD",
    font_color="FONT_IP_GOLD"
):
    display = init_display()
    from lib.display import pwm

    await fade_display_on()

    LED_PALETTE = PALETTES.get(theme_palette_name, PALETTES["IP_GOLD"])
    FONT_PALETTE = PALETTES.get(font_color, PALETTES["FONT_IP_GOLD"])

    led_group = getattr(led_map, section, led_map.all_leds)

    def get_color():
        return random.choice(LED_PALETTE)

    display_dirs = ["vertical", "horizontal", "center-out"]

    color_a = get_color()
    color_b = get_color()

    async def run_wave(led_group, reversed=False, color=None, dim=False, direction_override=None):
        np.fill((0, 0, 0))
        led_range = reversed and range(len(led_group) - 1, -1, -1) or range(len(led_group))

        display_dir = direction_override or random.choice(display_dirs)
        if display_dir == "horizontal":
            display_steps = SCREEN_HEIGHT // 4
        elif display_dir == "center-out":
            display_steps = SCREEN_HEIGHT // 2
        else:
            display_steps = SCREEN_WIDTH // 5

        max_steps = max(len(led_group), display_steps)

        for step in range(max_steps):
            if step < len(led_group):
                i = led_range[step]
                brightness = BRIGHTNESS * (1 - step / max_steps) if dim else BRIGHTNESS
                set_pixel(led_group[i], color, brightness)
                np.write()

            if step < display_steps:
                await draw_display_fill(step, display_steps, display_dir, get_color())

            await asyncio.sleep(speed)

    # Run multiple direction-changing passes
    await run_wave(led_group, reversed=False, color=color_a, direction_override="horizontal")
    await run_wave(led_group, reversed=True, color=color_b, direction_override="vertical")
    await run_wave(led_group, reversed=False, color=color_a, direction_override="center-out")

    await screen_corruption_cleanup(FONT_PALETTE)

    await run_wave(led_group, reversed=True, color=color_b, dim=True, direction_override="horizontal")

    await fade_leds_out()
    await fade_display_off()

if __name__ == "__main__":
    asyncio.run(wave_fx_runner(
        section="center_w_bottom",
        direction="top-to-bottom",
        speed=0.03,
        mirrored=True,
        theme_palette_name="IP_GOLD",
        font_color="FONT_IP_GOLD"
    ))
