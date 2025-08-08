import time, json, random, math
import uasyncio as asyncio
from config import DEFAULT_HANDLE, SETTINGS_FILE, SCREEN_WIDTH, SCREEN_HEIGHT, BL_BRIGHTNESS, FONT_COLOR, THEME_PALETTE_NAME
from fonts.palettes import PALETTES
from lib.display import init_display  # Import initializer

# Globals
display = None
FONT_PALETTE = PALETTES.get(FONT_COLOR, PALETTES[FONT_COLOR])

################################################ TEST below

from config import BRIGHTNESS, THEME_PALETTE_NAME, LED_PIN, LED_COUNT
from fonts.palettes import PALETTES
from machine import Pin
import neopixel
from patterns.led_map import all_leds

np = neopixel.NeoPixel(Pin(LED_PIN), LED_COUNT)
LED_PALETTE = PALETTES.get(THEME_PALETTE_NAME, [(255, 251, 0)])

def flash_glitch_leds(simultaneous=8):
    np.fill((0, 0, 0))  # Clear everything first
    for _ in range(simultaneous):
        i = random.choice(all_leds)
        r, g, b = random.choice(LED_PALETTE)
        np[i] = (int(r * BRIGHTNESS), int(g * BRIGHTNESS), int(b * BRIGHTNESS))
    np.write()

async def fade_leds_out(steps=5, delay=0.02):
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

################################################ TEST ^

def random_font_color():
    r, g, b = random.choice(FONT_PALETTE)
    return display.color(r, g, b)

def get_handle(force_default_chance=0.01):
    if random.random() < force_default_chance:
        return DEFAULT_HANDLE
    try:
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f).get("handle", DEFAULT_HANDLE)
    except Exception:
        return DEFAULT_HANDLE

# --- Layout Calculation ---
def compute_best_layout(text):
    for scale in range(6, 0, -1):
        char_w, char_h = 8 * scale, 8 * scale
        padding = 4
        one_line_width = len(text) * char_w

        if one_line_width <= SCREEN_WIDTH and char_h <= SCREEN_HEIGHT:
            return [text], scale, char_w, char_h, 0

        if ' ' in text:
            mid = min((abs(i - len(text)//2), i) for i, c in enumerate(text) if c == ' ')[1]
            l1, l2 = text[:mid].strip(), text[mid:].strip()
            w1, w2 = len(l1) * char_w, len(l2) * char_w
            total_h = 2 * char_h + padding
            if w1 <= SCREEN_WIDTH and w2 <= SCREEN_WIDTH and total_h <= SCREEN_HEIGHT:
                return [l1, l2], scale, char_w, char_h, padding

    return [text], 1, 8, 8, 0  # fallback

# --- Render Text ---
def draw_handle(lines, scale, char_w, char_h, padding):
    display.fill(display.color(0, 0, 0))
    total_h = len(lines) * char_h + (len(lines) - 1) * padding
    y_start = (SCREEN_HEIGHT - total_h) // 2

    for i, line in enumerate(lines):
        x_start = (SCREEN_WIDTH - len(line) * char_w) // 2
        y = y_start + i * (char_h + padding)
        for j, c in enumerate(line):
            display.upscaled_text(x_start + j * char_w, y, c, random_font_color(), upscaling=scale)

# --- Async Boot Flash ---
async def boot_flash_async():
    flash_glitch_leds()
    flash_color = display.color(255, 255, 255)
    display.fill(flash_color)
    await asyncio.sleep(0.07)
    flash_glitch_leds()
    display.fill(display.color(0, 0, 0))
    await asyncio.sleep(0.07)
    display.fill(flash_color)
    flash_glitch_leds()
    await asyncio.sleep(0.04)
    display.fill(display.color(0, 0, 0))
    await asyncio.sleep(0.1)

# --- Async Glitch Text Resolve ---
async def glitch_text_resolve_async(lines, scale, char_w, char_h, padding, duration=1.0):
    charset = "!@#$%^&*()_+=-[]{};:<>?|\\/"
    start = time.ticks_ms()
    total_h = len(lines) * char_h + (len(lines) - 1) * padding
    y_start = (SCREEN_HEIGHT - total_h) // 2

    glitch_state = [list(line) for line in lines]
    resolved = [[False for _ in line] for line in lines]

    while time.ticks_diff(time.ticks_ms(), start) < int(duration * 1000):
        display.fill(display.color(0, 0, 0))

        if random.random() < 0.3:
            flash_glitch_leds()

        for row_idx, line in enumerate(lines):
            x_start = (SCREEN_WIDTH - len(line) * char_w) // 2
            y = y_start + row_idx * (char_h + padding)

            for i, c in enumerate(line):
                if not resolved[row_idx][i]:
                    if random.random() < 0.2:
                        glitch_state[row_idx][i] = random.choice(charset)
                    elif random.random() < 0.05:
                        glitch_state[row_idx][i] = c
                        resolved[row_idx][i] = True

                display.upscaled_text(
                    x_start + i * char_w,
                    y,
                    glitch_state[row_idx][i],
                    random_font_color(),
                    upscaling=scale
                )

        await asyncio.sleep(0.05)

    draw_handle(lines, scale, char_w, char_h, padding)

# --- Async Static Glitch Boot ---
async def boot_glitch_static_async(duration=2, flash=True):
    flash_glitch_leds()
    display.fill(display.color(0, 0, 0))
    t_start = time.ticks_ms()
    noise_colors = PALETTES.get(FONT_COLOR, PALETTES["FONT_IP_GOLD"])

    while time.ticks_diff(time.ticks_ms(), t_start) < int(duration * 1000):
        display.fill(display.color(0, 0, 0))
        for _ in range(10):
            y = random.randint(0, SCREEN_HEIGHT - 1)
            h = random.randint(1, 4)
            x = random.randint(0, SCREEN_WIDTH // 2)
            w = random.randint(20, SCREEN_WIDTH - x)
            color = random.choice(noise_colors)
            display.rect(x, y, w, h, display.color(*color), fill=True)
        await asyncio.sleep(0.05)

    if flash:
        display.fill(display.color(255, 255, 255))
        await asyncio.sleep(0.08)
        display.fill(display.color(0, 0, 0))

    if random.random() < 0.3:
        flash_glitch_leds()

# Dim down the display to avoid it appearing "on" after run
async def fade_off():
    from lib.display import pwm  # Ensure we get the initialized global
    for level in reversed(range(0, BL_BRIGHTNESS + 1000, 1000)):
        pwm.duty_u16(min(level, BL_BRIGHTNESS))
        await asyncio.sleep(0.01)
    display.fill(display.color(0, 0, 0))

###############################################################

async def wave_distortion_async(duration=2):
    from config import FONT_COLOR
    from fonts.palettes import PALETTES

    glitch_palette = PALETTES.get(FONT_COLOR, PALETTES["FONT_IP_GOLD"])
    t_start = time.ticks_ms()

    while time.ticks_diff(time.ticks_ms(), t_start) < int(duration * 1000):
        display.fill(display.color(0, 0, 0))

        # Horizontal jitter wave
        for y_offset in range(0, SCREEN_HEIGHT, 5):
            amp = random.randint(2, 10)
            phase_shift = random.uniform(0, 2 * 3.14)
            color = display.color(*random.choice(glitch_palette))

            # Create a distorted horizontal bar
            for x in range(0, SCREEN_WIDTH, 10):
                jitter = int(amp * math.sin(0.15 * x + phase_shift))
                w = random.randint(6, 12)
                h = random.randint(1, 3)
                display.rect(
                    x + jitter,  # x distortion
                    y_offset,
                    w,
                    h,
                    color,
                    fill=True
                )

        await asyncio.sleep(0.04)

async def flash_and_fade_glitch_leds(simultaneous=8, steps=3, delay=0.01):
    for _ in range(simultaneous):
        i = random.choice(all_leds)
        r, g, b = random.choice(LED_PALETTE)
        np[i] = (int(r * BRIGHTNESS), int(g * BRIGHTNESS), int(b * BRIGHTNESS))
    np.write()

    # Rapid fade
    for s in reversed(range(1, steps)):
        for i in range(LED_COUNT):
            r, g, b = np[i]
            np[i] = (int(r * s / steps), int(g * s / steps), int(b * s / steps))
        np.write()
        await asyncio.sleep(delay)

async def color_scanline_flicker_async(duration=0.5, palette=None, min_delay=0.005, max_delay=0.03):
    """
    Glitchy horizontal scanline flicker using a color palette.

    Args:
        duration (float): how long the flicker should run.
        palette (list): list of (r, g, b) tuples. Falls back to grayscale glitchy tones.
        min_delay (float): shortest time between flickers.
        max_delay (float): longest time between flickers.
    """
    if palette is None:
        palette = [
            (255, 255, 255),  # white
            (192, 192, 192),  # light gray
            (255, 251, 0),    # IP_GOLD-style yellow
            (0, 0, 0),        # black for ghost lines
            (212, 175, 55),   # gold
        ]

    t_start = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), t_start) < int(duration * 1000):
        flash_glitch_leds()
        y = random.randint(0, SCREEN_HEIGHT - 1)
        h = random.randint(1, 3)  # line thickness
        color = display.color(*random.choice(palette))
        display.rect(0, y, SCREEN_WIDTH, h, color, fill=True)
        await asyncio.sleep(random.uniform(min_delay, max_delay))

###############################################################

# Run fun
async def handle_runner():
    global display
    display = init_display()

    try:
        handle = get_handle()
        lines, scale, char_w, char_h, padding = compute_best_layout(handle)

        await flash_and_fade_glitch_leds(simultaneous=10)
        await color_scanline_flicker_async(duration=1, palette=PALETTES["FONT_ALIEN_GREEN"])
        await asyncio.sleep(.5)
        await boot_glitch_static_async()
        await flash_and_fade_glitch_leds(simultaneous=10)
        await asyncio.sleep(.5)
        await glitch_text_resolve_async(lines, scale, char_w, char_h, padding, duration=4)
        await boot_flash_async()
        await flash_and_fade_glitch_leds(simultaneous=10)
        await wave_distortion_async() # not sure I'm gonna use this
        draw_handle(lines, scale, char_w, char_h, padding)
        await flash_and_fade_glitch_leds(simultaneous=80)
        await fade_leds_out()
        await asyncio.sleep(4)
        await fade_off()

    except Exception as e:
        print("[Display] Error:", e)

# Optional: standalone test
if __name__ == "__main__":
    asyncio.run(handle_runner())
