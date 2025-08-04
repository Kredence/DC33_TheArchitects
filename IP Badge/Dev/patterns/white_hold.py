import uasyncio as asyncio
from machine import Pin
import neopixel

from config import LED_PIN, LED_COUNT, BRIGHTNESS, BL_BRIGHTNESS
from lib.display import init_display
from patterns.led_map import all_leds

# Init display (shared globally)
display = init_display()

# Set up NeoPixel strip
np = neopixel.NeoPixel(Pin(LED_PIN), LED_COUNT)

# Adjust brightness to 20% of configured BRIGHTNESS
WHITE_BRIGHTNESS = BRIGHTNESS * 0.2

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

def scale_color(color, brightness):
    r, g, b = color
    return (int(r * brightness), int(g * brightness), int(b * brightness))

def set_leds_white():
    white = scale_color((255, 255, 255), WHITE_BRIGHTNESS)
    for i in all_leds:
        # Output in GRB order
        np[i] = (white[1], white[0], white[2])
    np.write()

def clear_leds():
    for i in range(LED_COUNT):
        np[i] = (0, 0, 0)
    np.write()

# --- Async Entry Point ---
async def run_white_hold():
    set_leds_white()
    await fade_display_on()

    display.fill(display.color(255, 255, 255))
    await asyncio.sleep(60)

    await fade_display_off()
    clear_leds()

if __name__ == "__main__":
    asyncio.run(run_white_hold())