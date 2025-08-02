import uasyncio as asyncio
import uselect, sys, os, urandom
# import sys
# import os
import ujson as json
# import urandom
# import utime
from config import DEFAULT_HANDLE
from fonts import palettes as p
USER_SETTINGS_FILE = "user_settings.json"
import config as CONFIG_PATH

HANDLE_FILE = "hacker_handle.json"

ASCII_ART = r"""

>>==================================================================================================<<
||  ___  ___       ___       ___  ___  _____ ______   ___  ________   ________  _________  ___      ||
|| |\  \|\  \     |\  \     |\  \|\  \|\   _ \  _   \|\  \|\   ___  \|\   __  \|\___   ___\\  \     ||
|| \ \  \ \  \    \ \  \    \ \  \\\  \ \  \\\__\ \  \ \  \ \  \\ \  \ \  \|\  \|___ \  \_\ \  \    ||
||  \ \  \ \  \    \ \  \    \ \  \\\  \ \  \\|__| \  \ \  \ \  \\ \  \ \   __  \   \ \  \ \ \  \   ||
||   \ \  \ \  \____\ \  \____\ \  \\\  \ \  \    \ \  \ \  \ \  \\ \  \ \  \ \  \   \ \  \ \ \  \  ||
||    \ \__\ \_______\ \_______\ \_______\ \__\    \ \__\ \__\ \__\\ \__\ \__\ \__\   \ \__\ \ \__\ ||
||     \|__|\|_______|\|_______|\|_______|\|__|     \|__|\|__|\|__| \|__|\|__|\|__|    \|__|  \|__| ||
||                          ________  ________  ________  _________    ___    ___                   ||
||                         |\   __  \|\   __  \|\   __  \|\___   ___\ |\  \  /  /|                  ||
||                         \ \  \|\  \ \  \|\  \ \  \|\  \|___ \  \_| \ \  \/  / /                  ||
||                          \ \   ____\ \   __  \ \   _  _\   \ \  \   \ \    / /                   ||
||                           \ \  \___|\ \  \ \  \ \  \\  \|   \ \  \   \/  /  /                    ||
||                            \ \__\    \ \__\ \__\ \__\\ _\    \ \__\__/  / /                      ||
||                             \|__|     \|__|\|__|\|__|\|__|    \|__|\___/ /                       ||
||                                                                                                  ||
||                           Welcome, traveler. The signal is strong.                               ||
||                                 The next phase begins now.                                       ||
>>==================================================================================================<<
"""

# --- Async Helpers ---

async def async_input(prompt=""):
    print(prompt, end="")  # no flush() in MicroPython
    poller = uselect.poll()
    poller.register(sys.stdin, uselect.POLLIN)
    while True:
        if poller.poll(0):
            return sys.stdin.readline().strip()
        await asyncio.sleep(0.05)

# --- Display ASCII art with scroll ---
async def scroll_ascii_art(ascii_art):
    lines = ascii_art.split('\n')
    for line in lines:
        print(line)
        delay_ms = urandom.getrandbits(8) % 300 + 50
        await asyncio.sleep_ms(delay_ms)

# --- Handle Management ---

def get_hacker_handle():
    if HANDLE_FILE in os.listdir():
        with open(HANDLE_FILE, "r") as f:
            data = json.load(f)
        return data.get("handle", DEFAULT_HANDLE)
    return DEFAULT_HANDLE

async def set_hacker_handle():
    handle = await async_input("Enter a new handle: ")
    if not handle:
        print("Handle unchanged.")
        return None
    with open(HANDLE_FILE, "w") as f:
        json.dump({"handle": handle}, f)
    print("Handle changed to:", handle)
    return handle

# --- Config Updaters ---
# Trying to update the user
def update_user_settings_field(field, value):
    try:
        settings = {}
        if USER_SETTINGS_FILE in os.listdir():
            with open(USER_SETTINGS_FILE, "r") as f:
                settings = json.load(f)

        settings[field] = value

        with open(USER_SETTINGS_FILE, "w") as f:
            json.dump(settings, f)

        print(f"{field} updated to {value}")
    except Exception as e:
        print("Error updating user_settings.json:", e)

async def set_font_palette():
    font_keys = [k for k in dir(p) if k.startswith("FONT_")]
    print("\nAvailable font palettes:")
    for i, k in enumerate(font_keys):
        print(f"{i+1}. {k}")
    choice = await async_input("Select number: ")
    try:
        index = int(choice) - 1
        selected = font_keys[index]
        update_user_settings_field("FONT_COLOR", repr(selected))  # ensure quoted string
    except Exception as e:
        print("Invalid choice:", e)

async def set_led_palette():
    led_keys = [k for k in dir(p) if not k.startswith("FONT_") and not k.startswith("__")]
    print("\nAvailable LED palettes:")
    for i, k in enumerate(led_keys):
        print(f"{i+1}. {k}")
    choice = await async_input("Select number: ")
    try:
        index = int(choice) - 1
        selected = led_keys[index]
        update_user_settings_field("THEME_PALETTE_NAME", repr(selected))  # ensure quoted string
    except Exception as e:
        print("Invalid choice:", e)

async def set_brightness():
    val = await async_input("Enter brightness (0.1 to 1.0): ")
    try:
        b = float(val)
        if 0.1 <= b <= 1.0:
            update_user_settings_field("BRIGHTNESS", str(b))
        else:
            print("Out of range.")
    except:
        print("Invalid value.")

# --- Menu ---

def show_menu():
    print("\nMenu Options:")
    print("1. Show handle")
    print("2. Change handle")
    print("3. Change font palette")
    print("4. Change LED color palette")
    print("5. Restart to apply changes")
    print("6. Exit")

async def run_menu():
    await scroll_ascii_art(ASCII_ART)
    handle = get_hacker_handle()
    print("\nWelcome, {}!".format(handle))

    while True:
        show_menu()
        choice = await async_input("Select an option: ")

        if choice == '1':
            handle = get_hacker_handle()
            print("Your handle is:", handle)

        elif choice == '2':
            new_handle = await set_hacker_handle()
            if new_handle:
                handle = new_handle

        elif choice == '3':
            await set_font_palette()

        elif choice == '4':
            await set_led_palette()

        elif choice == '5':
            print("Restarting now to apply changes...")
            await asyncio.sleep(1)
            import machine
            machine.reset()

        elif choice == '6':
            print("Exiting menu loop. Main app still running.")
            break

        else:
            print("Invalid choice. Try again.")

# Optional: for direct execution
if __name__ == "__main__":
    asyncio.run(run_menu())