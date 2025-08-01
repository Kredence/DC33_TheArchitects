# This holds all the info about the display and initizes it from here instead of the handle_display or gif_player since 
# that causes issues with async

from machine import Pin, SPI, PWM
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BL_BRIGHTNESS
import st7789_ext

display = None
pwm = None

def init_display():
    global display, pwm
    spi = SPI(0, baudrate=40000000, phase=1, polarity=1, sck=Pin(6), mosi=Pin(7))
    display = st7789_ext.ST7789(
        spi,
        SCREEN_WIDTH, SCREEN_HEIGHT,
        reset=Pin(3, Pin.OUT),
        dc=Pin(4, Pin.OUT),
        cs=Pin(5, Pin.OUT)
    )

    display.init(landscape=True, mirror_y=False, mirror_x=True, inversion=False, xstart=18, ystart=82)
    display.fill(display.color(0, 0, 0))

    pwm = PWM(Pin(2))
    pwm.freq(1000)
    pwm.duty_u16(BL_BRIGHTNESS)

    return display