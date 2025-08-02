import uasyncio as asyncio
import random
from patterns import handle_display,breathe, twinkle, chase, gif_player
from patterns.handle_display import run as display_run
from lib import utils
# from config import GIF_FOLDER
from menu import run_menu
from patterns.gif_player import run_gif

# Run on boot
# menu.main() # Gives a time-based menu for the user to set handle - this needs a way to gracefully exit

# Troubleshoot stuff
# from patterns import led_test
# led_test.run()

# Displays the users handle
async def display_loop():
    while True:
        try:
            # print("[Main] Starting display animation")
            await display_run()
        except Exception as e:
            print("[Main] Display task failed:", e)

        delay = random.randint(10, 30)
        # print(f"[Main] Next display run in {delay} seconds")
        await asyncio.sleep(delay)

# Sets what light patterns are running
async def run_lighting_loop():
    while True:
        await breathe.breathe(section="all_leds", loop_count=1)
        await twinkle.twinkle(count=4, section="sky")
        # await chase.chase(section="sky", direction="reverse")

# async def run_gif_loop():
#     await gif_player.run(folder=GIF_FOLDER, loop_count=1)
#     await asyncio.sleep(3)
    # await gif_player.(folder=GIF_FOLDER, loop_count=3, fade_on_done=True)

async def run_gif_loop():
    while True:
        await run_gif()
        await asyncio.sleep(random.randint(20, 40))

# Troublehsooting
# async def heartbeat():
#     while True:
#         print("Heartbeat: Event loop is alive")
#         await asyncio.sleep(2)

async def main():
    await asyncio.gather(
        display_loop(),
        run_lighting_loop(),
        run_menu(),
        # run_gif_loop()
    )

asyncio.run(main())