# Runs a light test for each section

from machine import Pin
import neopixel
from time import sleep
import random
from config import LED_PIN, LED_COUNT, BRIGHTNESS, THEME_PALETTE_NAME
import patterns.led_map as led_map
from fonts.palettes import PALETTES

# Set to True if you want randmo colors
use_random_colors = False

# Get the current theme palette from config
theme_palette = PALETTES.get(THEME_PALETTE_NAME, [(255, 255, 0)])

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
        if isinstance(i, int) and 0 <= i < LED_COUNT:
            np[i] = scale_color(color)
    np.write()
    sleep(3)
    fade_out()

# Automatically detect all list-type LED sections from led_map
def get_all_sections():
    section_list = []
    for name in dir(led_map):
        if name.startswith("__"):
            continue
        section = getattr(led_map, name)
        if isinstance(section, list) and all(isinstance(i, int) for i in section):
            if use_random_colors:
                color = tuple(random.randint(64, 255) for _ in range(3))
            else:
                color = random.choice(theme_palette)
            section_list.append((name, section, color))
    return section_list

def run():
    sections = get_all_sections()
    for name, section, color in sections:
        show_section(section, color, name)

    # Cleanup
    np.fill((0, 0, 0))
    np.write()

if __name__ == "__main__":
    run()