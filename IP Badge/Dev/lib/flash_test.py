from machine import SPI, Pin
import os
from lib.winbond import W25QFlash

# Setup SPI and CS for W25Q flash
spi = SPI(1, sck=Pin(10), mosi=Pin(11), miso=Pin(12))
cs = Pin(13, Pin.OUT)
flash = W25QFlash(spi=spi, cs=cs, baud=2000000)
mount_point = "/external"

# --- Mount Flash (format if needed) ---
try:
    os.mount(flash, mount_point)
except OSError:
    print("Formatting flash and creating filesystem...")
    os.VfsFat.mkfs(flash)
    os.mount(flash, mount_point)

# --- Show Flash Usage in Megabits ---
fs_stat = os.statvfs(mount_point)
bsize, blocks, free_blocks = fs_stat[0], fs_stat[2], fs_stat[3]

total_bytes = bsize * blocks
free_bytes = bsize * free_blocks
used_bytes = total_bytes - free_bytes

# Convert to megabits (Mb)
def to_megabits(bytes_val):
    return (bytes_val * 8) / (1024 * 1024)

print("Flash Total: {:.2f} Mb".format(to_megabits(total_bytes)))
print("Used Space: {:.2f} Mb".format(to_megabits(used_bytes)))
print("Free Space: {:.2f} Mb".format(to_megabits(free_bytes)))

# # --- Find Next Available File Numbers ---
existing_files = os.listdir(mount_point)
existing_numbers = []

for fname in existing_files:
    if fname.startswith("file_") and fname.endswith(".txt"):
        try:
            num = int(fname[5:-4])
            existing_numbers.append(num)
        except:
            pass

next_num = max(existing_numbers, default=-1) + 1

# --- Write 3 Unique Files ---
for i in range(3):
    filename = "file_{:03d}.txt".format(next_num + i)
    full_path = mount_point + "/" + filename
    with open(full_path, "w") as f:
        f.write("This is {}\n".format(filename))
    print("Wrote:", filename)