# config.py
import ujson as json

LED_PIN = 8
LED_COUNT = 83
BRIGHTNESS = 0.3 # This is specific to the LEDs, NOT the display backlighting
THEME_COLOR = (255, 251, 0)
SETTINGS_FILE = "hacker_handle.json"
DEFAULT_HANDLE = "Illuminati Party"
HACKER_HANDLE = ""
SCREEN_WIDTH = 284
SCREEN_HEIGHT = 76
BL_BRIGHTNESS = 65535  # 0–65535, adjust lower for dimmer (e.g., ~38%)
THEME_BITMAP_FONT = "vga2_8x16"  # Pick any font from /fonts/bitmap
DISPLAY_INTERVAL = 20
GLITCH_INTERVAL = 30
# FONT_COLOR = "FONT_DARK_ALIEN_GREEN" # Format this in quotes, check /fonts/palettes.py for the color options
# THEME_PALETTE_NAME = "ALIEN_GREEN" # This is called for the LED colors. Format this in quotes, check /fonts/palettes.py for the color options
FONT_COLOR = "" # Format this in quotes, check /fonts/palettes.py for the color options
THEME_PALETTE_NAME = "" # This is called for the LED colors. Format this in quotes, check /fonts/palettes.py for the color options

def _clean(val, default, cast=None):
    if val is None:
        return default
    if cast == float:
        try:
            return float(val)
        except:
            return default
    if isinstance(val, str):
        return val.strip("'\"")
    return val

try:
    with open("user_settings.json", "r") as f:
        _user_config = json.load(f)
        FONT_COLOR = _clean(_user_config.get("FONT_COLOR"), "FONT_DARK_ALIEN_GREEN")
        THEME_PALETTE_NAME = _clean(_user_config.get("THEME_PALETTE_NAME"), "ALIEN_GREEN")
except Exception as e:
    FONT_COLOR = "FONT_DARK_ALIEN_GREEN"
    THEME_PALETTE_NAME = "ALIEN_GREEN"