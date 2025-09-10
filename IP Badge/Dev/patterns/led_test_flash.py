# This take sections (found in the led_map.py), flashes them individually, then togehter, and loops x3

from machine import Pin
import neopixel
from time import sleep
import random
from config import LED_PIN, LED_COUNT, BRIGHTNESS, THEME_PALETTE_NAME
import patterns.led_map as led_map
from fonts.palettes import PALETTES

# Customize your section names here
selected_section_names = ["illuminati_letters","party_letters"]  # <- Update this list as needed

use_random_colors = False  # Set to True to randomize color per section
repeat_count = 3  # How many times to run the full cycle

# Theme palette
theme_palette = PALETTES.get(THEME_PALETTE_NAME, [(255, 255, 0)])

# Setup NeoPixel
np = neopixel.NeoPixel(Pin(LED_PIN), LED_COUNT)

def scale_color(color, brightness=BRIGHTNESS):
    r, g, b = color
    return (int(r * brightness), int(g * brightness), int(b * brightness))

def fade_out(delay=0.01, steps=10):
    for step in range(steps, -1, -1):
        factor = step / steps
        for i in range(LED_COUNT):
            r, g, b = np[i]
            np[i] = (int(r * factor), int(g * factor), int(b * factor))
        np.write()
        sleep(delay)

def show_section(led_indexes, color, label):
    print(f"Lighting section: {label}")
    np.fill((0, 0, 0))
    for i in led_indexes:
        if isinstance(i, int) and 0 <= i < LED_COUNT:
            np[i] = scale_color(color)
    np.write()
    sleep(2)
    fade_out()

def show_all_sections_combined(sections):
    print("Lighting all selected sections together")
    np.fill((0, 0, 0))
    for _, led_indexes, color in sections:
        for i in led_indexes:
            if isinstance(i, int) and 0 <= i < LED_COUNT:
                np[i] = scale_color(color)
    np.write()
    sleep(2)
    fade_out()

def get_selected_sections():
    section_data = []
    for name in selected_section_names:
        section = getattr(led_map, name, None)
        if isinstance(section, list):
            color = tuple(random.randint(64, 255) for _ in range(3)) if use_random_colors else random.choice(theme_palette)
            section_data.append((name, section, color))
    return section_data

def run():
    selected_sections = get_selected_sections()
    if not selected_sections:
        print("No valid sections found.")
        return

    for _ in range(repeat_count):
        for name, leds, color in selected_sections:
            show_section(leds, color, name)
        if len(selected_sections) > 1:
            show_all_sections_combined(selected_sections)

    # Final cleanup
    np.fill((0, 0, 0))
    np.write()

if __name__ == "__main__":
    run()