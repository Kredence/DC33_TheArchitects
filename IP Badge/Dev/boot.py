# This file is executed on every boot (including wake-boot from deepsleep)
# Mounts the filesystem to flash

from machine import SPI, Pin
import os
from lib.winbond import W25QFlash, version

os_info = os.uname()
print('MicroPython infos: {}'.format(os_info))
print('Used micropthon-winbond version: {}'.format(version.__version__))

# Pin assignments
SPI_ID = 1  # Change as appropriate for your board
spi = SPI(SPI_ID, sck=Pin(10), mosi=Pin(11), miso=Pin(12))  # Explicit pins
CS_PIN = Pin(13, Pin.OUT)

flash = W25QFlash(spi=spi, cs=CS_PIN, baud=2000000, software_reset=True)

# get Flash infos/properties
print("Flash manufacturer ID: 0x{0:02x}".format(flash.manufacturer))
print("Flash Memory Type: {}".format(flash.mem_type))
print("Flash Device Type: 0x{0:02x}".format(flash.device))
print("Flash size: {} bytes".format(flash.capacity))

flash_mount_point = '/external'

try:
    print('Mounting the external flash to "{}" ...'.format(flash_mount_point))
    os.mount(flash, flash_mount_point)
    print('External flash mounted to "{}"'.format(flash_mount_point))
except Exception as e:
    print('Failed to mount the external flash due to: {}'.format(e))

    if e.errno == 19:
        # [Errno 19] ENODEV aka "No such device"
        # create the filesystem, this takes some seconds (approx. 10 sec)
        print('Creating filesystem for external flash ...')
        print('This might take up to 10 seconds')
        os.VfsFat.mkfs(flash)
        print('Filesystem for external flash created')
    else:
        # takes some seconds/minutes (approx. 40 sec for 128MBit/16MB)
        print('Formatting external flash ...')
        print('This might take up to 60 seconds')
        # !!! only required on the very first start (will remove everything)
        flash.format()
        print('External flash formatted')

        # create the filesystem, this takes some seconds (approx. 10 sec)
        print('Creating filesystem for external flash ...')
        print('This might take up to 10 seconds')
        # !!! only required on first setup and after formatting
        os.VfsFat.mkfs(flash)
        print('Filesystem for external flash created')

    # finally mount the external flash
    os.mount(flash, flash_mount_point)
    print('External flash mounted to "{}"'.format(flash_mount_point))

print('boot.py steps completed')
