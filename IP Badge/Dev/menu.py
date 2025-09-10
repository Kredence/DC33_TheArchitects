import uasyncio as asyncio
import uselect, sys, os, urandom
import ujson as json
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

# Global reader for input
sreader = asyncio.StreamReader(sys.stdin)

BRIGHTNESS_PRESETS = [
    ("Default", 0.3),
    ("Brighter but not terrible", 0.5),
    ("Might need sunglasses", 0.7),
    ("MY EYES!", 1.0),
]

# --- Async Helpers ---
async def async_input(prompt=""):
    print(prompt, end="")
    line = await sreader.readline()
    return line.decode().strip()

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
    print("\nHandle changed to:", handle)
    show_current_settings()
    return handle

# --- Config Updaters ---

# This echos back the config change
def show_current_settings():
    try:
        if USER_SETTINGS_FILE in os.listdir():
            with open(USER_SETTINGS_FILE, "r") as f:
                settings = json.load(f)
            print("\n--- Current Settings ---")
            for k, v in settings.items():
                print(f"{k}: {v}")
            print("------------------------")
        else:
            print("\nNo user_settings.json yet.")
    except Exception as e:
        print("Error reading current settings:", e)

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
        show_current_settings()
    except Exception as e:
        print("Error updating user_settings.json:", e)

# Adding this so that the options for palettes only picks the values and not PALETTE as a bug fix
async def pick_from_list(title, options):
    if not options:
        print(f"\n{title}: none found.")
        return None
    print(f"\n{title}:")
    for i, k in enumerate(options, 1):
        print(f"{i}. {k}")
    choice = await async_input("Select number: ")
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(options):
            return options[idx]
    except:
        pass
    print("Invalid choice.")
    return None

# Font palette picker (uses only FONT_* entries from the dict)
async def set_font_palette():
    # Iterate over the dict keys, not module globals
    font_keys = sorted([k for k in p.PALETTES.keys() if k.startswith("FONT_")])
    selected = await pick_from_list("Available font palettes", font_keys)
    if selected:
        update_user_settings_field("FONT_COLOR", selected)

# LED palette picker (filters out FONT_* entries)
async def set_led_palette():
    led_keys = sorted([k for k in p.PALETTES.keys() if not k.startswith("FONT_")])
    selected = await pick_from_list("Available LED palettes", led_keys)
    if selected:
        update_user_settings_field("THEME_PALETTE_NAME", selected)

async def set_brightness():
    print("\nChoose a brightness level:")
    for i, (label, _) in enumerate(BRIGHTNESS_PRESETS):
        print(f"{i+1}. {label}")

    choice = await async_input("Select option: ")
    if not choice.isdigit():
        print("Invalid choice.")
        return

    index = int(choice) - 1
    if 0 <= index < len(BRIGHTNESS_PRESETS):
        label, value = BRIGHTNESS_PRESETS[index]
        update_user_settings_field("BRIGHTNESS", value)
        print(f"Brightness set to '{label}' ({value}).")
    else:
        print("Invalid choice.")

# --- Menu ---
def show_menu():
    print("\nMenu Options:")
    print("1. Show handle")
    print("2. Change handle")
    print("3. Change font palette")
    print("4. Change LED color palette")
    print("5. Change brightness")
    print("6. Restart to apply changes")
    print("7. Exit")

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
            await set_brightness()

        elif choice == '6':
            print("Restarting now to apply changes...")
            await asyncio.sleep(1)
            import machine
            machine.reset()

        elif choice == '7':
            print("Exiting menu loop. Main app still running.")
            break

        else:
            print("Invalid choice. Try again.")


# Optional: for direct execution
if __name__ == "__main__":
    asyncio.run(run_menu())