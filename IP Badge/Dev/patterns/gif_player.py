import time, uasyncio as asyncio
import os
from machine import Pin, SPI, PWM
from lib import st7789_ext
# from config import SCREEN_WIDTH, SCREEN_HEIGHT, BL_BRIGHTNESS
from lib.display import init_display

# Globals
display = None

# # --- Display Setup ---
# display = st7789_ext.ST7789(
#     SPI(0, baudrate=40000000, phase=1, polarity=1, sck=Pin(6), mosi=Pin(7)),
#     SCREEN_WIDTH, SCREEN_HEIGHT,
#     reset=Pin(3, Pin.OUT),
#     dc=Pin(4, Pin.OUT),
#     cs=Pin(5, Pin.OUT)
# )
# display.init(landscape=True, mirror_y=False, mirror_x=True, inversion=False, xstart=18, ystart=82)
# display.fill(display.color(0, 0, 0))  # Prevent white flash

# # --- Backlight Fade-In ---
# pwm = PWM(Pin(2))
# pwm.freq(1000)
# for level in range(0, BL_BRIGHTNESS + 1000, 1000):
#     pwm.duty_u16(min(level, BL_BRIGHTNESS))
#     time.sleep(0.01)

FOLDER = "/external/animations"
PREFIX = "frame_"
EXT = ".565"
DELAY = 0  # Seconds between frames

# --- Frame Discovery ---
def discover_frame_paths(folder=FOLDER, prefix=PREFIX, ext=EXT):
    try:
        files = os.listdir(folder)
        frame_files = [f for f in files if f.startswith(prefix) and f.endswith(ext)]
        # Extract numeric part and sort
        frames = sorted(
            frame_files,
            key=lambda f: int(f[len(prefix):-len(ext)])
        )
        return [f"{folder}/{f}" for f in frames]
    except Exception as e:
        print(f"Error reading folder '{folder}': {e}")
        return []

# --- Playback Loop ---
async def play_565_animation():
    frame_paths = discover_frame_paths()
    if not frame_paths:
        print("No valid frames found.")
        return

    while True:
        for path in frame_paths:
            try:
                display.image(0, 0, path)
            except Exception:
                pass  # Silently skip bad frames
            await asyncio.sleep(DELAY)

# --- Entry Point ---
async def run_gif():
    global display
    display = init_display()
    await play_565_animation()

if __name__ == "__main__":
    asyncio.run(run_gif())

# THIS WORKS ^^^^^^^^^^^^