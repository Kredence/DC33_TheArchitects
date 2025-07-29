import config
import ujson as json   # or just import json on normal Python
import os, urandom, utime
import time
from config import DEFAULT_HANDLE

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

HANDLE_FILE = "hacker_handle.json"
DEFAULT_HANDLE = "Anonymous"

def get_hacker_handle():
    # Check if the file exists
    if HANDLE_FILE in os.listdir():
        # Load existing handle
        with open(HANDLE_FILE, "r") as f:
            data = json.load(f)
        handle = data.get("handle", "").strip()
        if handle:
            return handle
    # If file doesn't exist or handle empty, prompt and save
    handle = input("Enter your handle: ").strip()
    if not handle:
        handle = DEFAULT_HANDLE
    with open(HANDLE_FILE, "w") as f:
        json.dump({"handle": handle}, f)
    return handle

def set_hacker_handle():
    handle = input("Enter a new handle: ").strip()
    if not handle:
        print("Handle unchanged.")
        return None
    with open(HANDLE_FILE, "w") as f:
        json.dump({"handle": handle}, f)
    print("Handle changed to:", handle)
    return handle

def show_menu():
    print("\nMenu Options:")
    print("1. Show handle")
    print("2. Change handle")
    print("3. Exit")

def scroll_ascii_art(ascii_art):
    lines = ascii_art.split('\n')
    for line in lines:
        print(line)
        # Random delay between 50ms and 350ms
        delay_ms = urandom.getrandbits(8) % 300 + 50
        utime.sleep_ms(delay_ms)

def main():
    scroll_ascii_art(ASCII_ART)
    handle = get_hacker_handle()
    print("\nWelcome, {}!".format(handle))

    while True:
        show_menu()
        choice = input("Select an option: ").strip()
        if choice == '1':
            with open(HANDLE_FILE, "r") as f:
                handle = json.load(f).get("handle", DEFAULT_HANDLE)
            print("Your handle is:", handle)
        elif choice == '2':
            new_handle = set_hacker_handle()
            if new_handle:
                handle = new_handle
        elif choice == '3':
            print("Exiting. Unplug or reset to restart.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
