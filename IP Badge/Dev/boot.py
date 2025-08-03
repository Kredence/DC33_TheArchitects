# # This file is executed on every boot (including wake-boot from deepsleep)
# # Mounts the filesystem to flash

# from machine import SPI, Pin
# import os
# from lib.winbond import W25QFlash, version
# from lib.utils import boot_flash_led

# # Uncomment this if you want version info
# # os_info = os.uname()
# # print('MicroPython infos: {}'.format(os_info))
# # print('Used micropthon-winbond version: {}'.format(version.__version__))

# # Pin assignments
# SPI_ID = 1  # Change as appropriate for your board
# spi = SPI(SPI_ID, sck=Pin(10), mosi=Pin(11), miso=Pin(12))  # Explicit pins
# CS_PIN = Pin(13, Pin.OUT)

# flash = W25QFlash(spi=spi, cs=CS_PIN, baud=2000000, software_reset=True)

# # # get Flash infos/properties
# # print("Flash manufacturer ID: 0x{0:02x}".format(flash.manufacturer))
# # print("Flash Memory Type: {}".format(flash.mem_type))
# # print("Flash Device Type: 0x{0:02x}".format(flash.device))
# # print("Flash size: {} bytes".format(flash.capacity))

# mount_point = '/external'
# animations_dir = mount_point + "/animations"

# # --- Mount Flash if not already mounted ---
# if 'external' not in os.listdir("/"):
#     try:
#         os.mount(flash, mount_point)
#         print("Flash mounted successfully at", mount_point)
#     except Exception as e:
#         print("Mount failed:", e)
#         print("Formatting flash, please wait...")
#         flash.format()
#         os.VfsFat.mkfs(flash)
#         os.mount(flash, mount_point)
#         print("Flash formatted and mounted at", mount_point)
# else:
#     print("Flash already mounted at", mount_point)

# # --- Show available space ---
# fs_stat = os.statvfs(mount_point)
# free_bytes = fs_stat[0] * fs_stat[3]
# print("Free space on flash: {:.2f} KB".format(free_bytes / 1024))

# # --- Ensure 'animations' directory exists ---
# if "animations" not in os.listdir(mount_point):
#     try:
#         os.mkdir(animations_dir)
#         print("Created directory:", animations_dir)
#     except Exception as e:
#         print("Failed to create animations directory:", e)
# else:
#     print("'animations' folder already exists")

# boot_flash_led() # sanity check onboard LED


# This file is executed on every boot (including wake-boot from deepsleep)
# Mounts the filesystem to flash


from machine import SPI, Pin
import os
from lib.winbond import W25QFlash, version
from lib.utils import boot_flash_led

from machine import SPI, Pin
import os,lib
from lib.winbond import W25QFlash, version
from lib.utils import boot_flash_led

# Pin assignments
SPI_ID = 1
spi = SPI(SPI_ID, sck=Pin(10), mosi=Pin(11), miso=Pin(12))
CS_PIN = Pin(13, Pin.OUT)

flash = W25QFlash(spi=spi, cs=CS_PIN, baud=2000000, software_reset=True)

mount_point = '/external'
animations_dir = mount_point + "/animations"
subdirs = ["hackers1", "hackers2", "dance"]

# --- Mount Flash if not already mounted ---
if 'external' not in os.listdir("/"):
    try:
        os.mount(flash, mount_point)
        print("Flash mounted successfully at", mount_point)
    except Exception as e:
        print("Mount failed:", e)
        print("Formatting flash, please wait...")
        flash.format()
        os.VfsFat.mkfs(flash)
        os.mount(flash, mount_point)
        print("Flash formatted and mounted at", mount_point)
else:
    print("Flash already mounted at", mount_point)

# --- Show available space ---
fs_stat = os.statvfs(mount_point)
free_bytes = fs_stat[0] * fs_stat[3]
print("Free space on flash: {:.2f} KB".format(free_bytes / 1024))

# --- Ensure 'animations' directory exists ---
if "animations" not in os.listdir(mount_point):
    try:
        os.mkdir(animations_dir)
        print("Created directory:", animations_dir)
    except Exception as e:
        print("Failed to create animations directory:", e)
else:
    print("'animations' folder already exists")

# --- Ensure subdirectories exist ---
for sub in subdirs:
    sub_path = animations_dir + f"/{sub}"
    try:
        if sub not in os.listdir(animations_dir):
            os.mkdir(sub_path)
            print("Created subdirectory:", sub_path)
        else:
            print(f"'{sub}' folder already exists")
    except Exception as e:
        print(f"Failed to create {sub_path}:", e)

boot_flash_led()  # sanity check onboard LED
