from time import sleep
import neopixel
from machine import Pin
from config import LED_PIN, LED_COUNT, BRIGHTNESS

# Optional: turn off onboard LED (Pin 16)
onboard = Pin(16, Pin.OUT)
onboard.value(0)

# Initialize NeoPixel strip
np = neopixel.NeoPixel(Pin(LED_PIN), LED_COUNT)

def test_led_numbering(delay=0.8, color=(255, 0, 0)):
    """Cycle through each LED with a brief red pulse and index printout."""
    print("Starting LED numbering test...")
    for i in range(LED_COUNT):
        np.fill((0, 0, 0))  # turn all off
        np[i] = tuple(int(c * BRIGHTNESS) for c in color)
        np.write()
        print(f"LED {i} ON")
        sleep(delay)
    np.fill((0, 0, 0))
    np.write()
    print("Test complete.")

# Run if executed directly
if __name__ == "__main__":
    test_led_numbering()
