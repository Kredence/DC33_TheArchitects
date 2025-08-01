import time, json, random
import uasyncio as asyncio
from config import DEFAULT_HANDLE, SETTINGS_FILE, SCREEN_WIDTH, SCREEN_HEIGHT, BL_BRIGHTNESS, FONT_COLOR
from fonts.palettes import PALETTES
from lib.display import init_display  # Import initializer

# Globals
display = None
FONT_PALETTE = PALETTES.get(FONT_COLOR, PALETTES[FONT_COLOR])

def random_font_color():
    r, g, b = random.choice(FONT_PALETTE)
    return display.color(r, g, b)

# --- Handle Loading ---
def get_handle():
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
    flash_color = display.color(255, 255, 255)
    display.fill(flash_color)
    await asyncio.sleep(0.07)
    display.fill(display.color(0, 0, 0))
    await asyncio.sleep(0.07)
    display.fill(flash_color)
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
    display.fill(display.color(0, 0, 0))
    t_start = time.ticks_ms()
    noise_colors = [
        (255, 255, 255),
        (255, 251, 0),
        (200, 200, 200),
        (212, 175, 55),
        (192, 192, 192),
        (40, 40, 40)
    ]

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

async def fade_off():
    from lib.display import pwm  # Ensure we get the initialized global
    for level in reversed(range(0, BL_BRIGHTNESS + 1000, 1000)):
        pwm.duty_u16(min(level, BL_BRIGHTNESS))
        await asyncio.sleep(0.01)
    display.fill(display.color(0, 0, 0))

# Run fun
async def run():
    global display
    display = init_display()

    try:
        handle = get_handle()
        lines, scale, char_w, char_h, padding = compute_best_layout(handle)

        await boot_glitch_static_async()
        await glitch_text_resolve_async(lines, scale, char_w, char_h, padding, duration=4)
        await boot_flash_async()
        draw_handle(lines, scale, char_w, char_h, padding)
        await asyncio.sleep(4)
        await fade_off()

    except Exception as e:
        print("[Display] Error:", e)

# Optional: standalone test
if __name__ == "__main__":
    asyncio.run(run())
