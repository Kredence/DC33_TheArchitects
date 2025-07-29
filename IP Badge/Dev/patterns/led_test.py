from machine import Pin
import neopixel
from time import sleep
from config import LED_PIN, LED_COUNT, BRIGHTNESS
from patterns.led_map import (
    left_sky, right_sky, beam, bottom, triangle_upper_mid,
    triangle_center_ring, triangle_lower_mid, triangle_left, triangle_right,
    triangle_lower, triangle_tip, triangle_bottom_wings, triangle,
    sky, all_leds,eye
)

# Set up NeoPixel strip
np = neopixel.NeoPixel(Pin(LED_PIN), LED_COUNT)

# Brightness-adjusted color helper
def scale_color(color, brightness=BRIGHTNESS):
    r, g, b = color
    return (int(r * brightness), int(g * brightness), int(b * brightness))

# Fade out effect for all LEDs
def fade_out(delay=0.01, steps=10):
    for step in range(steps, -1, -1):
        factor = step / steps
        for i in range(LED_COUNT):
            r, g, b = np[i]
            np[i] = (int(r * factor), int(g * factor), int(b * factor))
        np.write()
        sleep(delay)

# Turn on a section with a given color
def show_section(led_indexes, color, label):
    print(f"Testing section: {label}")
    np.fill((0, 0, 0))
    for i in led_indexes:
        if i < LED_COUNT:
            np[i] = scale_color(color)
    np.write()
    sleep(5)
    fade_out()

# List of (name, section, color)
sections = [
    ("left_sky", left_sky, (255, 0, 0)),
    ("right_sky", right_sky, (0, 255, 0)),
    ("beam", beam, (0, 0, 255)),
    ("bottom", bottom, (255, 255, 0)),
    ("triangle_upper_mid", triangle_upper_mid, (255, 0, 255)),
    ("triangle_center_ring", triangle_center_ring, (0, 255, 255)),
    # ("triangle_lower_mid", triangle_lower_mid, (255, 128, 0)),
    # ("triangle_left", triangle_left, (128, 0, 255)),
    # ("triangle", triangle, (0, 128, 255)),
    # ("mid_center", mid_center, (128, 255, 0)),
    # ("bottom_center", bottom_center, (255, 0, 128)),
    ("eye", eye, (255, 255, 255)),
    # ("bottom_skull", bottom_skull, (100, 100, 100)),
    # ("sky", sky, (0, 128, 128)),
    # ("all_leds", all_leds, (32, 32, 32)),
]

def run():
    # Run through all sections
    for name, section, color in sections:
        show_section(section, color, name)

    # Cleanup
    np.fill((0, 0, 0))
    np.write()

if __name__ == "__main__":
    run()