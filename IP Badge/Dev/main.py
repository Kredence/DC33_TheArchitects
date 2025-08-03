import uasyncio as asyncio
# import random
from patterns import handle_display,breathe, twinkle, chase, gif_player,breathe_fx,twinkle,wave_fx
# from lib import utils
from config import FONT_COLOR, THEME_PALETTE_NAME, BRIGHTNESS
from menu import run_menu
from patterns.gif_player import run_gif

# Run on boot
# menu.main() # Gives a time-based menu for the user to set handle - this needs a way to gracefully exit

async def main():
    while True:
        await handle_display.handle_runner()
        await asyncio.sleep(0.5)
        await wave_fx.wave_fx_runner(
            section="triangle",direction="top-to-bottom",speed=0.03,mirrored=True,
            theme_palette_name="CYBERPUNK_VIOLET", font_color="FONT_DARK_LETTERS")
        await asyncio.sleep(0.5)
        await breathe_fx.breathe(
            section="center_w_bottom",loop_count=2,simultaneous=5,color_ramp=True,randomize_speed=True,
            min_brightness=0.1,max_brightness=BRIGHTNESS,easing="sine",led_palette_name=THEME_PALETTE_NAME,font_palette_name=FONT_COLOR)
        await asyncio.sleep(0.5)
        await twinkle.twinkle(count=30,speed=0.03,simultaneous=1,section="bottom",randomize_speed=False,color_ramp=False)
        await asyncio.sleep(0.5)

if __name__ == "__main__":
    asyncio.run(main())