# This file is executed on every boot (including wake-boot from deepsleep)
# import esp
# esp.osdebug(None)
# import webrepl
# webrepl.start()

from machine import SPI, Pin
import os, vfs
from lib.winbond import W25QFlash, version

force_format = True

os_info = os.uname()
print('MicroPython infos: {}'.format(os_info))
print('Used micropthon-winbond version: {}'.format(version.__version__))

# try:
#     if 'pyboard' in os_info:
#         # NOT YET TESTED !
#         # https://docs.micropython.org/en/latest/library/pyb.SPI.html#pyb.SPI
#         CS_PIN = Pin(1)
#         spi = SPI(1)
#     elif 'esp8266' in os_info:
#         # NOT YET TESTED !
#         # https://docs.micropython.org/en/latest/esp8266/quickref.html#hardware-spi-bus
#         # SPI(0) is used for FlashROM and not available to users
#         # highest possible baudrate is 40 MHz for ESP-12
#         CS_PIN = Pin(1)
#         spi = SPI(1)
#     elif 'esp32' in os_info:
#         # https://docs.micropython.org/en/latest/esp32/quickref.html#hardware-spi-bus
#         # Pin   HSPI (id=1)   VSPI (id=2)
#         # -------------------------------
#         # sck   14            18
#         # mosi  13            23
#         # miso  12            19
#         # cs    x, here 5     x, here 5
#         if 'esp32s3' in os_info.machine.lower():
#             CS_PIN = Pin(10)
#             spi = SPI(2, 2000000, sck=Pin(12), mosi=Pin(11), miso=Pin(13))
#         else:
#             CS_PIN = Pin(5)
#             spi = SPI(2)
#     elif 'rp2' in os_info:
#         # https://docs.micropython.org/en/latest/rp2/quickref.html#hardware-spi-bus
#         # Pin   id=0   id=1
#         # -------------------------------
#         # sck   6            10
#         # mosi  7            11
#         # miso  4            8
#         # cs    x, here 5    x, here 5
#         CS_PIN = Pin(5)
#         spi = SPI(0)
#     else:
#         raise Exception(
#             'Unknown device, no default values for CS_PIN and spi defined: {}'.
#             format(os_info)
#         )
# except AttributeError:
#     pass
# except Exception as e:
#     raise e

# Pin assignments
SPI_ID = 1
spi = SPI(SPI_ID, sck=Pin(10), mosi=Pin(11), miso=Pin(12))  # Explicit pins
CS_PIN = Pin(13, Pin.OUT)

flash = W25QFlash(spi=spi, cs=CS_PIN, baud=2000000, software_reset=True)

# get Flash infos/properties
print("Flash manufacturer ID: 0x{0:02x}".format(flash.manufacturer))
print("Flash Memory Type: {}".format(flash.mem_type))
print("Flash Device Type: 0x{0:02x}".format(flash.device))
print("Flash size: {} bytes".format(flash.capacity))

mount_point = "/external"

# Get flash info
print("MicroPython:", os.uname())
print("micropython-winbond:", version.__version__)
print("Flash ID: 0x{:02X}, Type: {}, Capacity: {} bytes".format(
    flash.manufacturer, flash.mem_type, flash.capacity
))

# Attempt to mount if not already mounted
if "external" not in os.listdir("/"):
    try:
        os.mount(flash, mount_point)
        print("Flash mounted at", mount_point)
    except OSError as e:
        print("Mount failed:", e)

        if e.errno == 19:  # ENODEV
            print("Creating new filesystem...")
            os.VfsFat.mkfs(flash)
        else:
            print("Formatting and creating new filesystem (one-time)...")
            flash.format()
            os.VfsFat.mkfs(flash)

        # Try mount again
        try:
            os.mount(flash, mount_point)
            print("Flash mounted at", mount_point)
        except Exception as e2:
            print("Failed to mount even after formatting:", e2)
else:
    print("Flash already mounted")

print("=== boot.py done ===\n")