import neopixel
import machine
import time

NUM_LEDS = 83
LED_PIN = 8          # WS2812B data pin
BRIGHTNESS = 0.7     # Range: 0.0 (off) to 1.0 (full brightness)
ONBOARD_LED_PIN = 16 # Onboard LED

np = neopixel.NeoPixel(machine.Pin(LED_PIN), NUM_LEDS)

def scaled_color(r, g, b, brightness):
    return (
        int(r * brightness),
        int(g * brightness),
        int(b * brightness)
    )

def flash_led_strip(brightness=0.2, times=1, delay=0.5):
    np = neopixel.NeoPixel(machine.Pin(LED_PIN), NUM_LEDS)

    # Cycle through colors
    colors = [
        (255, 0, 0),   # Green
        (0, 255, 0),   # Red
        (0, 0, 255)    # Blue
    ]

    for base_color in colors:
        scaled = scaled_color(*base_color, brightness)
        for _ in range(times):
            np.fill(scaled)
            np.write()
            time.sleep(delay)
            np.fill((0, 0, 0))
            np.write()
            time.sleep(delay)

def boot_flash_led(times=3, delay=0.2):
    led = neopixel.NeoPixel(machine.Pin(ONBOARD_LED_PIN), 1)
    for _ in range(times):
        led[0] = (0, 0, 255)  # blue
        led.write()
        time.sleep(delay)
        led[0] = (0, 0, 0)    # off
        led.write()
        time.sleep(delay)

def run():
    flash_led_strip()
    boot_flash_led()

# run()