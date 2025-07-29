from machine import Pin
from time import sleep
import uasyncio as asyncio
from lib import utils
from patterns import handle_display
import neopixel
from config import LED_PIN,LED_COUNT,BRIGHTNESS
import menu

# Run on boot
utils.boot_flash_led() # sanity check onboard LED
# menu.main() # Gives a time-based menu for the user to set handle - this needs a way to gracefully exit

# Init LED strip
np = neopixel.NeoPixel(Pin(LED_PIN), LED_COUNT)

# Troubleshoot stuff
# from patterns import led_test
# led_test.run()

import uasyncio as asyncio
from config import LED_PIN, LED_COUNT, BRIGHTNESS
from patterns import handle_display
from patterns import breathe, twinkle, chase  # Add other patterns here

# Run the startup sequence from handle_display
async def run_display_loop(interval=10):
    await handle_display.run()
    while True:
        await asyncio.sleep(interval)
        await handle_display.run()

# Cycle through your lighting patterns
async def run_lighting_loop():
    while True:
        await breathe.breathe(section="all_leds", loop_count=4, simultaneous=5, color_ramp=True, min_brightness=0.05, max_brightness=BRIGHTNESS)
        await asyncio.sleep(0.5)
        await twinkle.twinkle(count=6, section="sky", randomize_speed=True)
        await asyncio.sleep(0.5)
        await chase.chase(section="sky", direction="reverse", simultaneous=4, color_ramp=True)
        await asyncio.sleep(0.5)
        await twinkle.twinkle(count=3, section="all_leds", randomize_speed=False)

        # Add more patterns as needed

# Entry point
def main():
    try:
        asyncio.run(asyncio.gather(
            run_display_loop(),
            run_lighting_loop()
        ))
    except KeyboardInterrupt:
        print("Interrupted")

# Boot
if __name__ == "__main__":
    main()

# Send it
# main()