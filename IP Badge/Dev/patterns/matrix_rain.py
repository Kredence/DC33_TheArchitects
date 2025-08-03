import uasyncio as asyncio
import random, time
from machine import Pin
import neopixel
from config import LED_PIN, LED_COUNT, BRIGHTNESS, SCREEN_WIDTH, SCREEN_HEIGHT, BL_BRIGHTNESS
from lib.display import init_display
from fonts.palettes import PALETTES
from patterns import led_map

np = neopixel.NeoPixel(Pin(LED_PIN), LED_COUNT)

# --- Random Palette Helper ---
def pick_random_palette():
    font_keys = [k for k in PALETTES if k.startswith("FONT_")]
    if not font_keys:
        return PALETTES["IP_GOLD"], PALETTES["FONT_IP_GOLD"]

    font_key = random.choice(font_keys)
    led_key = font_key.replace("FONT_", "")
    return PALETTES.get(led_key, PALETTES["IP_GOLD"]), PALETTES[font_key]

# --- Fade + Setup Helpers ---
def set_pixel(i, color, brightness=1.0):
    r, g, b = color
    np[i] = (int(r * brightness), int(g * brightness), int(b * brightness))

async def fade_leds_out(steps=6, delay=0.03):
    for step in reversed(range(steps + 1)):
        for i in range(LED_COUNT):
            r, g, b = np[i]
            np[i] = (
                int(r * step / steps),
                int(g * step / steps),
                int(b * step / steps)
            )
        np.write()
        await asyncio.sleep(delay)

async def fade_display_on(target=BL_BRIGHTNESS, step=2000, delay=0.01):
    from lib.display import pwm
    for level in range(0, target + step, step):
        pwm.duty_u16(min(level, target))
        await asyncio.sleep(delay)

async def fade_display_off():
    from lib.display import pwm, display
    for level in reversed(range(0, BL_BRIGHTNESS + 2000, 2000)):
        pwm.duty_u16(min(level, BL_BRIGHTNESS))
        await asyncio.sleep(0.01)
    display.fill(display.color(0, 0, 0))

async def glitch_flash_section(section, color, brightness=1.0, flashes=3, delay=1):
    for _ in range(flashes):
        for i in section:
            set_pixel(i, color, brightness)
        np.write()
        await asyncio.sleep(delay)
        for i in section:
            np[i] = (0, 0, 0)
        np.write()
        await asyncio.sleep(delay)

# --- Fast Display Rain Loop ---
async def matrix_display_rain(font_color, duration=6):
    from lib.display import display
    charset = "|./\\Iil!01"
    scale = 2
    char_w = 8 * scale
    cols = SCREEN_WIDTH // char_w

    # t_start = asyncio.get_event_loop().time()
    t_start = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), t_start) < int(duration * 1000):
    # while asyncio.get_event_loop().time() - t_start < duration:
        display.fill(display.color(0, 0, 0))
        for _ in range(cols // 2):
            x = random.randint(0, SCREEN_WIDTH - char_w)
            y = random.randint(0, SCREEN_HEIGHT - 8)
            char = random.choice(charset)
            color = display.color(*font_color)
            display.upscaled_text(x, y, char, color, upscaling=scale)
        await asyncio.sleep(0.05)

# --- LED Rain Pass ---
async def matrix_led_rain(led_group, color, brightness=1.0, direction="top-to-bottom"):
    count = len(led_group)
    indexes = led_group if direction == "top-to-bottom" else list(reversed(led_group))

    for i in range(count):
        if random.random() < 0.2:
            continue  # skip a few to add irregularity
        set_pixel(indexes[i], color, brightness)
        np.write()
        await asyncio.sleep(0.07)

# --- Main Function ---
async def matrix_rain(
    section="all_leds",
    direction="top-to-bottom",
    led_color=None,
    font_color=None,
    brightness=None
):
    display = init_display()
    await fade_display_on()

    brightness = brightness or BRIGHTNESS
    # Pick random palette if not provided
    led_palette, font_palette = pick_random_palette()
    color = led_color or random.choice(led_palette)
    font_color = font_color or random.choice(font_palette)

    led_group = getattr(led_map, section, led_map.all_leds)
    if direction == "bottom-to-top":
        led_group = list(reversed(led_group))

    # Start fast screen rain effect in background
    display_task = asyncio.create_task(matrix_display_rain(font_color, duration=6))

    # Start LED rain with stagger
    await matrix_led_rain(led_group, color, brightness=brightness, direction=direction)

    await display_task

    # Glitch flash + ramp up
    glitch_color = random.choice(led_palette)
    await glitch_flash_section(led_map.eye + led_map.bottom, glitch_color, brightness=1.0, flashes=4, delay=0.05)
    for level in range(int(brightness * 10), 11):
        for i in led_map.eye + led_map.bottom:
            set_pixel(i, glitch_color, level / 10)
        np.write()
        await asyncio.sleep(0.02)
        await fade_display_off()
        

    await asyncio.sleep(0.4)
    await fade_leds_out()

# --- Test Run ---
if __name__ == "__main__":
    asyncio.run(matrix_rain())
