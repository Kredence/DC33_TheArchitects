import uasyncio as asyncio
import neopixel
import random
import urandom
import math
from machine import Pin

from config import LED_PIN, LED_COUNT, BRIGHTNESS, BL_BRIGHTNESS
from fonts.palettes import PALETTES
from patterns import led_map
from lib.display import init_display

# --- LED Setup ---
np = neopixel.NeoPixel(Pin(LED_PIN), LED_COUNT)

def set_pixel(i, color, brightness=1.0):
    # Palette colors are (R,G,B), strip is GRB
    r, g, b = color
    np[i] = (int(g * brightness), int(r * brightness), int(b * brightness))

def scale_pixel(i, factor):
    # Read GRB, scale, write GRB
    g, r, b = np[i]
    np[i] = (int(g * factor), int(r * factor), int(b * factor))

def eased(level, easing="linear"):
    t = level / 100
    if easing == "sine":
        return math.sin(t * math.pi / 2)
    return t

async def final_fade_out():
    steps = 5
    for level in reversed(range(steps + 1)):
        factor = level / steps
        for i in range(LED_COUNT):
            scale_pixel(i, factor)
        np.write()
        await asyncio.sleep(0.01)
    np.fill((0, 0, 0))
    np.write()

async def fade_display_on(target=BL_BRIGHTNESS, step=2000, delay=0.01):
    from lib.display import pwm
    for level in range(0, target + step, step):
        pwm.duty_u16(min(level, BL_BRIGHTNESS))
        await asyncio.sleep(delay)

async def fade_display_off(final_fill=True):
    from lib.display import pwm, display
    for level in reversed(range(0, BL_BRIGHTNESS + 2000, 2000)):
        pwm.duty_u16(min(level, BL_BRIGHTNESS))
        await asyncio.sleep(0.01)
    if final_fill:
        display.fill(display.color(0, 0, 0))

async def display_glitch_effect(brightness_level, font_palette):
    from lib.display import display, SCREEN_WIDTH, SCREEN_HEIGHT

    # 1. Jittery glitch blocks
    for _ in range(int(1 + brightness_level * 5)):
        w = random.randint(8, 50)
        h = random.randint(3, 12)
        x = random.randint(0, SCREEN_WIDTH - w)
        y = random.randint(0, SCREEN_HEIGHT - h)
        color = display.color(*random.choice(font_palette))
        display.rect(x, y, w, h, color, fill=True)

    # 2. Horizontal scanline tears
    for _ in range(2):
        y = random.randint(0, SCREEN_HEIGHT - 1)
        h = random.randint(1, 2)
        scan_color = display.color(*random.choice(font_palette))
        display.rect(0, y, SCREEN_WIDTH, h, scan_color, fill=True)

    # 3. Character flicker (glitch chars)
    glitch_chars = "!@#$%^&*()_+-=[]{}|<>~"
    scale = 2
    char_w = 8 * scale
    char_h = 8 * scale
    for _ in range(2):
        c = random.choice(glitch_chars)
        x = random.randint(0, SCREEN_WIDTH - char_w)
        y = random.randint(0, SCREEN_HEIGHT - char_h)
        color = display.color(*random.choice(font_palette))
        display.upscaled_text(x, y, c, color, upscaling=scale)

    await asyncio.sleep(0.01 + urandom.getrandbits(2) * 0.002)


# --- Main Breathe Pattern ---
async def breathe(
    section="all_leds",
    loop_count=3,
    simultaneous=4,
    color_ramp=False,
    randomize_speed=False,
    fade_out=True,
    min_brightness=0.1,
    max_brightness=0.3,
    easing="sine",
    led_palette_name="IP_GOLD",
    font_palette_name="FONT_IP_GOLD"
):
    # Setup LED group and palettes
    led_group = getattr(led_map, section, led_map.all_leds)
    LED_PALETTE = PALETTES.get(led_palette_name, PALETTES["IP_GOLD"])
    FONT_PALETTE = PALETTES.get(font_palette_name, PALETTES["FONT_IP_GOLD"])

    # Display Init
    init_display()
    from lib.display import pwm, display
    await fade_display_on()

    def get_next_color(palette, ramp_index):
        if color_ramp:
            color = palette[ramp_index % len(palette)]
            return color, ramp_index + 1
        else:
            return random.choice(palette), ramp_index

    ramp_index = 0
    for _ in range(loop_count):
        # --- Fade In ---
        for level in range(0, 101, 4):
            current_brightness = min_brightness + eased(level, easing) * (max_brightness - min_brightness)
            for _ in range(simultaneous):
                i = random.choice(led_group)
                color, ramp_index = get_next_color(LED_PALETTE, ramp_index)
                set_pixel(i, color, brightness=current_brightness)
            np.write()

            await display_glitch_effect(current_brightness, FONT_PALETTE)
            await asyncio.sleep(0.02 + (urandom.getrandbits(3) * 0.002 if randomize_speed else 0))

        # --- Fade Out ---
        for level in reversed(range(0, 101, 4)):
            current_brightness = min_brightness + eased(level, easing) * (max_brightness - min_brightness)
            for _ in range(simultaneous):
                i = random.choice(led_group)
                color, ramp_index = get_next_color(LED_PALETTE, ramp_index)
                set_pixel(i, color, brightness=current_brightness)
            np.write()

            await display_glitch_effect(current_brightness, FONT_PALETTE)
            await asyncio.sleep(0.02 + (urandom.getrandbits(3) * 0.002 if randomize_speed else 0))

    if fade_out:
        await final_fade_out()
        await fade_display_off()

# --- Test ---
if __name__ == "__main__":
    asyncio.run(breathe(
        section="center_w_bottom",
        loop_count=5,
        simultaneous=6,
        color_ramp=False,
        randomize_speed=True,
        min_brightness=0.1,
        max_brightness=0.6,
        easing="sine",
        led_palette_name="DARK_ALIEN_GREEN",
        font_palette_name="FONT_DARK_ALIEN_GREEN"
    ))
