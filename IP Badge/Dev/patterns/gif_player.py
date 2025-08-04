# import time, uasyncio as asyncio
# import os
# from machine import Pin, SPI, PWM
# from lib import st7789_ext
# from lib.display import init_display

# # Globals
# display = None

# FOLDER = "/external/animations/hackers1"
# PREFIX = "frame_"
# EXT = ".565"
# DELAY = 0  # Seconds between frames

# # --- Frame Discovery ---
# def discover_frame_paths(folder=FOLDER, prefix=PREFIX, ext=EXT):
#     try:
#         files = os.listdir(folder)
#         frame_files = [f for f in files if f.startswith(prefix) and f.endswith(ext)]
#         # Extract numeric part and sort
#         frames = sorted(
#             frame_files,
#             key=lambda f: int(f[len(prefix):-len(ext)])
#         )
#         return [f"{folder}/{f}" for f in frames]
#     except Exception as e:
#         print(f"Error reading folder '{folder}': {e}")
#         return []

# # --- Playback Loop ---
# async def play_565_animation():
#     frame_paths = discover_frame_paths()
#     if not frame_paths:
#         print("No valid frames found.")
#         return

#     while True:
#         for path in frame_paths:
#             try:
#                 display.image(0, 0, path)
#             except Exception:
#                 pass  # Silently skip bad frames
#             await asyncio.sleep(DELAY)

# # --- Entry Point ---
# async def gif_runner():
#     global display
#     display = init_display()
#     await play_565_animation()

# if __name__ == "__main__":
#     asyncio.run(gif_runner())

# # THIS WORKS ^^^^^^^^^^^^

import time, uasyncio as asyncio
import os
from machine import Pin, SPI, PWM
from lib import st7789_ext
from lib.display import init_display, pwm
from config import BL_BRIGHTNESS

# Globals
display = None

# Defaults
PREFIX = "frame_"
EXT = ".565"
DELAY = 0  # Seconds between frames

# --- Frame Discovery ---
def discover_frame_paths(folder, prefix=PREFIX, ext=EXT):
    try:
        files = os.listdir(folder)
        frame_files = [f for f in files if f.startswith(prefix) and f.endswith(ext)]
        frames = sorted(
            frame_files,
            key=lambda f: int(f[len(prefix):-len(ext)])
        )
        return [f"{folder}/{f}" for f in frames]
    except Exception as e:
        print(f"Error reading folder '{folder}': {e}")
        return []

# --- Fade Helpers ---
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

# --- Playback Loop ---
async def play_565_animation(folder):
    frame_paths = discover_frame_paths(folder)
    if not frame_paths:
        print("No valid frames found.")
        await fade_display_off()
        return

    await fade_display_on()
    for path in frame_paths:
        try:
            display.image(0, 0, path)
        except Exception:
            pass  # Silently skip bad frames
        await asyncio.sleep(DELAY)
    await fade_display_off()

# --- Entry Point ---
async def gif_runner(folder="/external/animations/messwiththebest"):
    global display
    display = init_display()
    await play_565_animation(folder)

# --- Test Hook ---
if __name__ == "__main__":
    asyncio.run(gif_runner("/external/animations/allyourbases1"))
