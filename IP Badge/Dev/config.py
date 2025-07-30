# config.py
LED_PIN = 8
LED_COUNT = 83
BRIGHTNESS = 0.5 # This is specific to the LEDs, NOT the display backlighting
THEME_COLOR = (255, 251, 0)
SETTINGS_FILE = "hacker_handle.json"
DEFAULT_HANDLE = "Illuminati Party"
HACKER_HANDLE = ""
SCREEN_WIDTH = 284
SCREEN_HEIGHT = 76
BL_BRIGHTNESS = 65000  # 0–65535, adjust lower for dimmer (e.g., ~38%)
FONT_COLOR = "FONT_IP_GOLD" # Format this in quotes, check /fonts/palettes.py for the color options
THEME_BITMAP_FONT = "vga2_8x16"  # Pick any font from /fonts/bitmap
DISPLAY_INTERVAL = 20
GLITCH_INTERVAL = 30
THEME_PALETTE_NAME = "DARK_ALIEN_GREEN" # This is called for the LED colors. Format this in quotes, check /fonts/palettes.py for the color options