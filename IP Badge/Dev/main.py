import uasyncio as asyncio
from patterns import handle_display, twinkle, gif_player, breathe_fx, twinkle, wave_fx, chase, matrix_rain, glitch_fx, eye_pulse,ajax,white_hold
from config import FONT_COLOR, THEME_PALETTE_NAME, BRIGHTNESS
from menu import run_menu


async def main():
    asyncio.create_task(run_menu())

    while True:
        await handle_display.handle_runner()
        await asyncio.sleep(4.5)
        await wave_fx.wave_fx_runner(
            section="center_w_bottom",direction="top-to-bottom",speed=0.03,mirrored=True,
            theme_palette_name=THEME_PALETTE_NAME, font_color=FONT_COLOR)
        await gif_player.gif_runner(folder="/external/animations/messwiththebest")
        await asyncio.sleep(4.5)
        await glitch_fx.glitch_sequence(section="bottom", style="wipe")
        await asyncio.sleep(4.5)
        await chase.chase(
            delay=0.01,simultaneous=4,section="sky",direction="bounce",loop_count=2,dual_head=True,color_ramp=True,randomize_speed=False)
        await asyncio.sleep(4.5)
        await breathe_fx.breathe(
            section="triangle",loop_count=2,simultaneous=5,color_ramp=True,randomize_speed=True,
            min_brightness=0.1,max_brightness=BRIGHTNESS,easing="sine",led_palette_name="NEON_BLUE_TEAL",font_palette_name="FONT_GHOST_GLITCH")
        await asyncio.sleep(4.5)
        await twinkle.twinkle(count=30,speed=0.03,simultaneous=1,section="bottom",randomize_speed=False,color_ramp=False)
        await asyncio.sleep(4.5)
        await matrix_rain.matrix_rain(section="center_beam")
        await asyncio.sleep(4.5)
        await glitch_fx.glitch_sequence(section="center_beam", style="wipe")
        await asyncio.sleep(4.5)
        await chase.chase(
            delay=0.01,simultaneous=2,section="center_beam",direction="forward",loop_count=2,dual_head=True,color_ramp=True,randomize_speed=False)
        await asyncio.sleep(4.5)
        await breathe_fx.breathe(
            section="all_leds",loop_count=2,simultaneous=10,color_ramp=True,randomize_speed=True,
            min_brightness=0.1,max_brightness=BRIGHTNESS,easing="sine",led_palette_name=THEME_PALETTE_NAME,font_palette_name=FONT_COLOR)
        await asyncio.sleep(4.5)
        await chase.chase(
            delay=0.01,simultaneous=4,section="sky",direction="reverse",loop_count=2,dual_head=False,color_ramp=True,randomize_speed=False)
        await asyncio.sleep(4.5)
        await gif_player.gif_runner(folder="/external/animations/allyourbases")
        await asyncio.sleep(4.5)
        await twinkle.twinkle(count=30,speed=0.03,simultaneous=1,section="all_leds",randomize_speed=False,color_ramp=False)
        await asyncio.sleep(4.5)
        await chase.chase(
            delay=0.01,simultaneous=7,section="beam_w_triangle",direction="bounce",loop_count=2,dual_head=True,color_ramp=True,randomize_speed=False)
        await asyncio.sleep(4.5)
        await eye_pulse.pulse_from_eye()
        await asyncio.sleep(4.5)
        await ajax.ajax_flash()
        await asyncio.sleep(4.5)

# Uncomment this section below if you need to run the LED/Display test
# async def main():
#     while True:
#         await white_hold.run_white_hold()

if __name__ == "__main__":
    asyncio.run(main())