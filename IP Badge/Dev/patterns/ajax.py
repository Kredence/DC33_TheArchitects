# patterns/ajax.py

import uasyncio as asyncio
import random
import neopixel
from machine import Pin
from config import LED_PIN, LED_COUNT, BRIGHTNESS, THEME_PALETTE_NAME, BL_BRIGHTNESS
from lib.display import init_display
from fonts.palettes import PALETTES
from patterns import led_map

# Set up NeoPixel strip
np = neopixel.NeoPixel(Pin(LED_PIN), LED_COUNT)

# --- Fade Helpers ---
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

# --- LED Helpers ---
def set_all_leds(color, brightness=BRIGHTNESS):
    r, g, b = color
    for i in range(LED_COUNT):
        np[i] = (int(g * brightness), int(r * brightness), int(b * brightness))  # GRB order
    np.write()

def clear_leds():
    for i in range(LED_COUNT):
        np[i] = (0, 0, 0)
    np.write()

# --- Pattern Main ---
async def ajax_flash(flashes=5, flash_delay=0.05):
    display = init_display()
    await fade_display_on()

    palette = PALETTES.get(THEME_PALETTE_NAME, PALETTES["IP_GOLD"])
    color = random.choice(palette)

    for _ in range(flashes):
        set_all_leds(color)
        display.fill(display.color(*color))
        await asyncio.sleep(flash_delay)

        clear_leds()
        display.fill(display.color(0, 0, 0))
        await asyncio.sleep(flash_delay)

    await asyncio.sleep(0.2)
    await fade_display_off()
    clear_leds()

# --- Run for Test ---
if __name__ == "__main__":
    asyncio.run(ajax_flash())