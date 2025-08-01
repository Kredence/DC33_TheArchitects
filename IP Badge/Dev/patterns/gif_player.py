# import time, uasyncio as asyncio
# from machine import Pin, SPI, PWM
# from lib import st7789_ext
# from config import SCREEN_WIDTH, SCREEN_HEIGHT, BL_BRIGHTNESS
# from patterns.twinkle import twinkle_loop  # Optional lighting effect

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

# FOLDER = "/external/animations"
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
# async def run():
#     await play_565_animation()

# if __name__ == "__main__":
#     asyncio.run(run())

# # THIS WORKS ^^^^^^^^^^^^

import uasyncio as asyncio
import os, time
from machine import Pin, SPI, PWM
from lib import st7789_ext
# from config import SCREEN_WIDTH, SCREEN_HEIGHT, BL_BRIGHTNESS
from config import BL_BRIGHTNESS,GIF_FOLDER

SCREEN_WIDTH = 282
SCREEN_HEIGHT = 74

# FOLDER = "/external/animations"
PREFIX = "frame_"
EXT = ".565"
DELAY = 0.08  # seconds between frames

# # --- Display Setup ---
# display = st7789_ext.ST7789(
#     SPI(0, baudrate=40_000_000, phase=1, polarity=1, sck=Pin(6), mosi=Pin(7)),
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

# --- Stream from Disk to Framebuffer ---
# --- Playback Loop: stream files from flash ---
# async def stream_565_from_flash():
#     try:
#         files = sorted([
#             f for f in os.listdir(FOLDER)
#             if f.startswith(PREFIX) and f.endswith(EXT)
#         ], key=lambda name: int(name[len(PREFIX):-len(EXT)]))

#         if not files:
#             print("No frames found.")
#             return

#         while True:
#             for f in files:
#                 path = f"{FOLDER}/{f}"
#                 try:
#                     display.image(0, 0, path)
#                 except Exception as e:
#                     print(f"Failed to load {f}: {e}")
#                 await asyncio.sleep(DELAY)

#     except Exception as e:
#         print(f"Streaming error: {e}")

# # --- Entry Point ---
# async def run():
#     await stream_565_from_flash()

# if __name__ == "__main__":
#     asyncio.run(run())

# # --- Playback Loop ---
# async def stream_565_from_flash(folder="/external/animations", loop_count=None):
#     try:
#         files = sorted([
#             f for f in os.listdir(folder)
#             if f.startswith(PREFIX) and f.endswith(EXT)
#         ], key=lambda name: int(name[len(PREFIX):-len(EXT)]))

#         if not files:
#             print(f"No frames found in {folder}")
#             return

#         loop = 0
#         while loop_count is None or loop < loop_count:
#             for f in files:
#                 path = f"{folder}/{f}"
#                 try:
#                     display.image(0, 0, path)
#                 except Exception as e:
#                     print(f"Failed to load {f}: {e}")
#                 await asyncio.sleep(DELAY)
#             loop += 1

#     except Exception as e:
#         print(f"Streaming error: {e}")

# # --- Main Entry Point ---
# async def run(folder=FOLDER, loop_count=2):
#     await stream_565_from_flash(folder=folder, loop_count=loop_count)

# # --- Manual CLI ---
# if __name__ == "__main__":
#     asyncio.run(run())

# # --- Backlight Control ---
# pwm = PWM(Pin(2))
# pwm.freq(1000)


# --- Backlight Pin (off during init) ---
bl_pin = Pin(2, Pin.OUT)
bl_pin.value(0)  # ensure backlight stays off before setup

# --- Display Setup ---
display = st7789_ext.ST7789(
    SPI(0, baudrate=40_000_000, phase=1, polarity=1, sck=Pin(6), mosi=Pin(7)),
    SCREEN_WIDTH, SCREEN_HEIGHT,
    reset=Pin(3, Pin.OUT),
    dc=Pin(4, Pin.OUT),
    cs=Pin(5, Pin.OUT)
)
display.init(landscape=True, mirror_y=False, mirror_x=True, inversion=False, xstart=18, ystart=82)
display.fill(display.color(0, 0, 0))  # paint black before enabling backlight

# --- Backlight PWM Setup ---
pwm = PWM(bl_pin)
pwm.freq(1000)
pwm.duty_u16(0)  # still off

# --- Fade On Later ---
def fade_on():
    for level in range(0, BL_BRIGHTNESS + 1000, 1000):
        pwm.duty_u16(min(level, BL_BRIGHTNESS))
        time.sleep(0.01)



# def fade_on():
#     for level in range(0, BL_BRIGHTNESS + 1000, 1000):
#         pwm.duty_u16(min(level, BL_BRIGHTNESS))
#         time.sleep(0.01)

def fade_off():
    for level in reversed(range(0, BL_BRIGHTNESS + 1000, 1000)):
        pwm.duty_u16(min(level, BL_BRIGHTNESS))
        time.sleep(0.01)
    display.fill(display.color(0, 0, 0))

# Playback
async def stream_565_from_flash(folder=GIF_FOLDER, loop_count=1):
    try:
        files = sorted([
            f for f in os.listdir(folder)
            if f.startswith(PREFIX) and f.endswith(EXT)
        ], key=lambda name: int(name[len(PREFIX):-len(EXT)]))

        if not files:
            print("No frames found in", folder)
            return

        fade_on()

        for _ in range(loop_count):
            for f in files:
                path = f"{folder}/{f}"
                try:
                    display.image(0, 0, path)
                except Exception as e:
                    print(f"Failed to load {f}: {e}")
                await asyncio.sleep(DELAY)

        fade_off()

    except Exception as e:
        print(f"Streaming error: {e}")

# Main async - setting the loop=0 run forever
async def run(folder=GIF_FOLDER, loop_count=1):
    await stream_565_from_flash(folder, loop_count)

# test run
if __name__ == "__main__":
    asyncio.run(run())