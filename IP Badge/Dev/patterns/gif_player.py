import time, uasyncio as asyncio
from machine import Pin, SPI, PWM
from lib import st7789_ext
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BL_BRIGHTNESS
from patterns.twinkle import twinkle_loop  # Optional lighting effect

# --- Display Setup ---
display = st7789_ext.ST7789(
    SPI(0, baudrate=40000000, phase=1, polarity=1, sck=Pin(6), mosi=Pin(7)),
    SCREEN_WIDTH, SCREEN_HEIGHT,
    reset=Pin(3, Pin.OUT),
    dc=Pin(4, Pin.OUT),
    cs=Pin(5, Pin.OUT)
)
display.init(landscape=True, mirror_y=False, mirror_x=True, inversion=False, xstart=18, ystart=82)
display.fill(display.color(0, 0, 0))  # Prevent white flash

# --- Backlight Fade-In ---
pwm = PWM(Pin(2))
pwm.freq(1000)
for level in range(0, BL_BRIGHTNESS + 1000, 1000):
    pwm.duty_u16(min(level, BL_BRIGHTNESS))
    time.sleep(0.01)

FOLDER = "/external/animations"
PREFIX = "frame-"
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
async def run():
    await play_565_animation()

if __name__ == "__main__":
    asyncio.run(run())

# THIS WORKS ^^^^^^^^^^^^


# # --- Frame Dimensions (based on .565 file size) ---
# ANIM_WIDTH = 273  # Not 286
# EXPECTED_FRAME_SIZE = ANIM_WIDTH * ANIM_HEIGHT * 2  # = 42564
# DELAY = 0.12  # seconds between frames
# START_FRAME = 0
# END_FRAME = 5  # inclusive, loads frame-0 to frame-10

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

# # --- Preload Frames ---
# def load_frames_to_ram():
#     frames = []
#     for i in range(START_FRAME, END_FRAME + 1):
#         path = f"{FOLDER}/{PREFIX}{i}{EXT}"
#         try:
#             with open(path, "rb") as f:
#                 buf = f.read()
#                 if len(buf) != EXPECTED_FRAME_SIZE:
#                     print(f"Skipping {path}: wrong size ({len(buf)} bytes)")
#                     continue
#                 frames.append(buf)
#         except Exception as e:
#             print(f"Failed to load {path}: {e}")
#     return frames

# # --- Playback Loop ---
# async def play_frames_from_ram(frames, center=True):
#     x_offset = (SCREEN_WIDTH - ANIM_WIDTH) // 2 if center else 0
#     y_offset = (SCREEN_HEIGHT - ANIM_HEIGHT) // 2 if center else 0

#     while True:
#         for buf in frames:
#             try:
#                 display.image(x_offset, y_offset, buf=buf, width=ANIM_WIDTH, height=ANIM_HEIGHT, filename=buf)
#             except Exception:
#                 pass
#             await asyncio.sleep(DELAY)

# # --- Main Run ---
# async def run():
#     frames = load_frames_to_ram()
#     if not frames:
#         print("No valid frames loaded into RAM.")
#         return

#     await asyncio.gather(
#         play_frames_from_ram(frames, center=True),
#         twinkle_loop(section="sky", simultaneous=3, fade_steps=5, randomize_speed=True)
#     )

# if __name__ == "__main__":
#     asyncio.run(run())