import os
from random import randint, uniform
from threading import Thread
from time import perf_counter, sleep
from typing import Union
from win32api import GetSystemMetrics  # type: ignore[import-untyped]
import win32gui  # type: ignore[import-untyped]

from pyautogui import press, pixel  # type: ignore[import-untyped]
from pynput.keyboard import Key, KeyCode, Listener  # type: ignore[import-untyped]
from dotenv import find_dotenv, load_dotenv, set_key  # type: ignore[import-not-found]

# Initial setup
os.system("cls")
load_dotenv()
print("\n" + "=" * 60)
print("  GENSHIN IMPACT - DIALOGUE AUTO-SKIPPER")
print("=" * 60)
print("  Version 2.1.8 | Keyboard & Mouse Edition")
print("=" * 60 + "\n")


COORDS = {
    "gamepad": {
        "default": {}
    },
    "mnk": {
        "default": {
            "LOADING_SCREEN_X": ("width_adjust", 1200),
            "LOADING_SCREEN_Y": ("height_adjust", 700),

            # Top-Left Permanent Dialogue Control Bar (Log, Hide UI, Audio, Autoplay)
            "PLAYING_ICON_X": ("width_adjust", 84),
            "PLAYING_ICON_Y": ("height_adjust", 46),
            "LOG_ICON_X": ("width_adjust", 140),
            "LOG_ICON_Y": ("height_adjust", 45),
            "HIDE_UI_ICON_X": ("width_adjust", 180),
            "HIDE_UI_ICON_Y": ("height_adjust", 45),
            "AUDIO_ICON_X": ("width_adjust", 218),
            "AUDIO_ICON_Y": ("height_adjust", 45),

            # Right-Side Dialogue Choice Options (Speech bubble 💬 & [F] box)
            "DIALOGUE_CHOICE_X": ("width_adjust", 1285),
            "DIALOGUE_F_BOX_X": ("width_adjust", 1235),

            # Bottom Dialogue Name & Golden Divider
            "CHAR_NAME_X": ("width_adjust", 960),
            "CHAR_NAME_Y": ("height_adjust", 810),
            "GOLDEN_DIVIDER_Y": ("height_adjust", 835),

            # Bottom-Center Yellow Diamond Indicator (Cutscenes & Narrations)
            "YELLOW_INDICATOR_X": ("width_adjust", 960)
        },
        "wide_screen": {
            "PLAYING_ICON_X": ("get_position_left", 84, 230),

            "DIALOGUE_ICON_X": ("get_position_right", 1301, 2770, 0.02),
            "DIALOGUE_ICON_LOWER_Y": ("height_adjust", 810),
            "DIALOGUE_ICON_HIGHER_Y": ("height_adjust", 792)
        },
        (2880, 1800): {
            "PLAYING_ICON_X": ("static", 126),

            "DIALOGUE_ICON_X": ("static", 1947),
            "DIALOGUE_ICON_LOWER_Y": ("static", 1370),
            "DIALOGUE_ICON_HIGHER_Y": ("static", 1260)
        }
    }
}


def width_adjust(x: int) -> int:
    """Adjust variables to the width of the screen."""
    return int(x / 1920 * SCREEN_WIDTH)


def height_adjust(y: int) -> int:
    """Adjust variables to the height of the screen."""
    return int(y / 1080 * SCREEN_HEIGHT)


def get_position_right(
    hdpos_x: int, doublehdpos_x: int, SCREEN_WIDTH: int, extra: float
) -> int:
    """
    Use this if the pixel is bound to the right side.
    Calculates the distance of the pixel from the right side of the screen. Returns position of pixel on x.
    """
    if SCREEN_WIDTH <= 3840:  # above 3840 we need an extra multiplier
        extra = 0
    diff = doublehdpos_x - hdpos_x
    change_per_pixel = diff / 1920
    screen_diff = SCREEN_WIDTH - 1920
    extra_pixels = screen_diff * (change_per_pixel + extra)
    position = int(hdpos_x + extra_pixels)
    return position


def get_position_left(hdpos_x: int, doublehdpos_x: int, SCREEN_WIDTH: int) -> int:
    """
    Use this if the pixel is bound to the left side.
    Calculates the distance of the pixel from the left side of the screen. Returns position of pixel on x
    """
    diff = doublehdpos_x - hdpos_x
    change_per_pixel = diff / 1920
    screen_diff = SCREEN_WIDTH - 1920
    extra_pixels = screen_diff * change_per_pixel
    position = int(hdpos_x + extra_pixels)
    return position


# Check if screen is 16:9 ratio
def is_screen_default_ratio() -> bool:
    if SCREEN_WIDTH > 1920 and float(int(SCREEN_HEIGHT) / int(SCREEN_WIDTH)) != float(0.5625):
        return False
    else:
        return True


def get_pixel(device: str, res: tuple[int,int], name: str):
    base = COORDS[device]["default"]
    override: dict = {}
    if res in COORDS[device]:
        override = COORDS[device].get(res, {})
    elif not is_screen_default_ratio():
        override = COORDS[device].get("wide_screen", {})

    merged = {**base, **override}

    if merged[name][0] == "width_adjust":
        return width_adjust(merged[name][1])
    if merged[name][0] == "height_adjust":
        return height_adjust(merged[name][1])
    if merged[name][0] == "get_position_left":
        x = get_position_left(merged[name][1], merged[name][2], res[0])
        if x > 231:
            x = 230
        return x
    if merged[name][0] == "get_position_right":
        return get_position_right(merged[name][1], merged[name][2], res[0], merged[name][3])
    if merged[name][0] == "static":
        return merged[name][1]

    raise ValueError(f"Unknown coord handler: {merged[name][0]} for {device}.{name}")



# Check if either screen dimension is missing from .env
if os.environ.get("WIDTH", "") == "" or os.environ.get("HEIGHT", "") == "" or os.environ.get("CONFIRM_BUTTON", "") == "" or os.environ.get("DEVICE", "") == "":
    # Detect and set screen dimensions
    SCREEN_WIDTH = GetSystemMetrics(0)
    SCREEN_HEIGHT = GetSystemMetrics(1)
    CONFIRM_BUTTON = "f" # F by default
    DEVICE = "mnk" # mouse n keyboard by default

    print(f"  Resolution: {SCREEN_WIDTH}x{SCREEN_HEIGHT}\n")

    while True:
        temp_conf_btn = str(input("Enter your in game interaction key (f.e: F):"))
        if len(temp_conf_btn) == 1:
            CONFIRM_BUTTON = str(temp_conf_btn.lower())
            break
        else:
            print("Incorrect format. Make sure it's only 1 character.")

    # Write changes to .env file
    dotenv_file = find_dotenv()
    if dotenv_file:
        set_key(dotenv_file, "WIDTH", str(SCREEN_WIDTH), quote_mode="never")
        set_key(dotenv_file, "HEIGHT", str(SCREEN_HEIGHT), quote_mode="never")
        set_key(dotenv_file, "CONFIRM_BUTTON", str(CONFIRM_BUTTON), quote_mode="never")
        set_key(dotenv_file, "DEVICE", str(DEVICE), quote_mode="never")
    else:
        # Create .env file if it doesn't exist
        with open(".env", "w") as f:
            f.write(f"WIDTH={SCREEN_WIDTH}\n")
            f.write(f"HEIGHT={SCREEN_HEIGHT}\n")
            f.write(f"CONFIRM_BUTTON={CONFIRM_BUTTON}\n")
            f.write(f"DEVICE={DEVICE}\n")
else:
    # Read screen dimensions from .env
    width_str = os.getenv("WIDTH")
    height_str = os.getenv("HEIGHT")
    if width_str is None or height_str is None:
        raise ValueError("WIDTH or HEIGHT environment variable is None")
    SCREEN_WIDTH = int(width_str)
    SCREEN_HEIGHT = int(height_str)

    CONFIRM_BUTTON = os.getenv("CONFIRM_BUTTON")
    DEVICE = os.getenv("DEVICE")

    print(f"Current resolution: {SCREEN_WIDTH}x{SCREEN_HEIGHT}\nChosen device: {DEVICE}\nCurrent interaction key: {CONFIRM_BUTTON}")

res = (SCREEN_WIDTH, SCREEN_HEIGHT)


def random_f_key_interval() -> float:
    """
    Return a random interval mimicking human rapid key presses (8-12 clicks/presses per second).
    Interval range: 0.080 - 0.125 seconds.
    """
    return uniform(0.080, 0.125)


def is_yellow_color(color: tuple[int, int, int]) -> bool:
    """Check if RGB color matches the yellow/gold diamond indicator ('◇' / '◆') or character name."""
    r, g, b = color[0], color[1], color[2]
    return bool(r >= 170 and g >= 120 and b <= 110 and r > g)


def is_light_grey_or_white(color: tuple[int, int, int]) -> bool:
    """Check if RGB color matches the F-key box UI element (light grey/white box background)."""
    r, g, b = color[0], color[1], color[2]
    return bool(r >= 210 and g >= 210 and b >= 210 and abs(int(r) - int(g)) <= 20 and abs(int(g) - int(b)) <= 20)


def is_valid_dialogue_choice(choice_x: int, y_pt: int) -> bool:
    """
    Validates that a white pixel at choice_x is a true dialogue pill option,
    and NOT a light-colored modal popup or menu background (Anti-False Positive).
    """
    try:
        # 1. Check if the icon pixel is white/light-grey
        icon_pixel = pixel(choice_x, y_pt)
        if not is_light_grey_or_white(icon_pixel):
            return False

        # 2. Check adjacent pill background pixel (35px to the right)
        # In a true dialogue choice, the pill background is dark translucent (RGB < 130).
        # In a modal popup or inventory parchment, the entire background is solid light/white (RGB > 160).
        bg_pixel = pixel(choice_x + width_adjust(35), y_pt)
        r, g, b = bg_pixel[0], bg_pixel[1], bg_pixel[2]

        # If the adjacent background is ALSO light/white, it is a modal/menu popup, NOT a dialogue choice!
        if r > 160 and g > 160 and b > 160:
            return False

        return True
    except Exception:
        return False


def should_take_break() -> bool:
    """
    Determine if we should take an occasional break.
    1 in 25 chance (4%) of taking a break.
    :return: True if we should take a break
    """
    return randint(1, 25) == 1


def take_random_break() -> float:
    """
    Take a random break between 3-8 seconds.
    :return: Duration of the break in seconds
    """
    break_duration = uniform(3.0, 8.0)
    print(f"  Taking a {break_duration:.1f}s break...")
    return break_duration


class MainStatus:
    """Class to hold the status of the main loop."""

    def __init__(self) -> None:
        self.status: str = "pause"


main_status = MainStatus()


def on_press(key: Union[Key, KeyCode, None]) -> None:
    """
    Start, stop, or exit the program based on the key pressed.
    :param key: The key pressed.
    :return: None
    """
    key_pressed = str(key)

    if key_pressed == "Key.f8":
        main_status.status = "run"
        print("\n" + "=" * 50)
        print("  STATUS: RUNNING")
        print("  Auto-skip is now ACTIVE")
        print("=" * 50 + "\n")
    elif key_pressed == "Key.f9":
        main_status.status = "pause"
        print("\n" + "=" * 50)
        print("  STATUS: PAUSED")
        print("  Auto-skip is now INACTIVE")
        print("=" * 50 + "\n")
    elif key_pressed == "Key.f12":
        main_status.status = "exit"
        print("\n" + "=" * 50)
        print("  Shutting down... Goodbye!")
        print("=" * 50 + "\n")
        exit()


def main() -> None:
    """
    Automatically press F key when dialogue is detected in Genshin Impact.
    Uses original dialogue detection logic but replaces clicks with F key presses.
    Includes random delays and occasional breaks for natural behavior.
    :return: None
    """

    def is_genshin_impact_active() -> bool:
        """Check if Genshin Impact is the active window using native Win32 API (ultra-fast)."""
        try:
            hwnd = win32gui.GetForegroundWindow()
            return win32gui.GetWindowText(hwnd) == "Genshin Impact"
        except Exception:
            return False

    def get_dialogue_state() -> tuple[bool, bool]:
        """
        Check dialogue state in a fast screenshot pass using PERMANENT UI elements.
        Detects:
          1. Loading Screen (Safety protection)
          2. Right-side dialogue choice options (multi-point vertical scan covering 1, 2, 3 options)
          3. Top-left permanent control bar (Autoplay, Log ≡, Hide UI 👁️, Audio 🔊)
          4. Bottom character name & golden divider line (Y ≈ 810-835)
          5. Bottom-center yellow diamond symbol (◇ / ◆, Y ≈ 910-960)
        Returns: (dialogue_active: bool, options_available: bool)
        """
        try:
            # 1. Confirm loading screen is not white (Safety)
            if pixel(get_pixel(DEVICE, res, "LOADING_SCREEN_X"), get_pixel(DEVICE, res, "LOADING_SCREEN_Y")) == (255, 255, 255):
                return False, False

            # 2. Check Right-Side Dialogue Choice Options (Speech bubble 💬 & [F] box)
            #    Scans vertical range with Dark Pill Contrast Check to reject modal/menu popups
            choice_x = get_pixel(DEVICE, res, "DIALOGUE_CHOICE_X")
            f_box_x = get_pixel(DEVICE, res, "DIALOGUE_F_BOX_X")
            choice_y_points = [
                height_adjust(710),
                height_adjust(735),
                height_adjust(750),
                height_adjust(770),
                height_adjust(790),
                height_adjust(808),
                height_adjust(830)
            ]
            for y_pt in choice_y_points:
                if is_valid_dialogue_choice(choice_x, y_pt) or is_valid_dialogue_choice(f_box_x, y_pt):
                    return True, True

            # 3. Check Top-Left Permanent Dialogue Control Bar Icons (Log ≡, Hide UI 👁️, Audio 🔊, Autoplay)
            log_x = get_pixel(DEVICE, res, "LOG_ICON_X")
            log_y = get_pixel(DEVICE, res, "LOG_ICON_Y")
            hide_x = get_pixel(DEVICE, res, "HIDE_UI_ICON_X")
            hide_y = get_pixel(DEVICE, res, "HIDE_UI_ICON_Y")
            audio_x = get_pixel(DEVICE, res, "AUDIO_ICON_X")
            audio_y = get_pixel(DEVICE, res, "AUDIO_ICON_Y")
            playing_x = get_pixel(DEVICE, res, "PLAYING_ICON_X")
            playing_y = get_pixel(DEVICE, res, "PLAYING_ICON_Y")

            if is_light_grey_or_white(pixel(log_x, log_y)) or is_light_grey_or_white(pixel(hide_x, hide_y)) or is_light_grey_or_white(pixel(audio_x, audio_y)):
                return True, False
            if pixel(playing_x, playing_y) == (236, 229, 216):
                return True, False

            # 4. Check Bottom Character Name & Golden Divider Line (Y ≈ 810 - 835)
            char_name_x = get_pixel(DEVICE, res, "CHAR_NAME_X")
            char_name_y = get_pixel(DEVICE, res, "CHAR_NAME_Y")
            divider_y = get_pixel(DEVICE, res, "GOLDEN_DIVIDER_Y")
            for x_offset in range(-60, 61, 20):
                if is_yellow_color(pixel(char_name_x + x_offset, char_name_y)) or is_yellow_color(pixel(char_name_x + x_offset, divider_y)):
                    return True, False

            # 5. Check Yellow Diamond Symbol ('◇' / '◆') at bottom-center (Cutscenes & Narrations)
            center_x = get_pixel(DEVICE, res, "YELLOW_INDICATOR_X")
            y_scan_points = [
                height_adjust(910),
                height_adjust(925),
                height_adjust(940),
                height_adjust(950),
                height_adjust(960)
            ]
            for y_pt in y_scan_points:
                if is_yellow_color(pixel(center_x, y_pt)):
                    return True, False

            return False, False
        except Exception:
            return False, False

    main_status.status = "pause"
    last_f_press = 0.0
    next_f_interval = random_f_key_interval()

    # Break tracking
    last_break_check = perf_counter()
    break_check_interval = 30.0  # Check for breaks every 30 seconds

    print("\n" + "=" * 60)
    print("  READY TO START")
    print("=" * 60)
    print("  Controls:")
    print("    [F8]  - Start Auto-Skip")
    print("    [F9]  - Pause Auto-Skip")
    print("    [F12] - Exit Program")
    print("=" * 60)
    print("\n  Waiting for input...\n")

    was_active = True

    while True:
        current_time = perf_counter()

        # Handle pause state
        while main_status.status == "pause":
            sleep(0.05)
            current_time = perf_counter()  # Update time after pause
            last_f_press = current_time  # Reset timing after pause
            was_active = True

        # Handle exit
        if main_status.status == "exit":
            break

        # Smart Auto-Pause: Only proceed if Genshin Impact is active (ultra-fast 30ms polling)
        if not is_genshin_impact_active():
            if was_active:
                print("  [SMART AUTO-PAUSE] Genshin Impact window lost focus. Auto-skip suspended.")
                was_active = False
            sleep(0.03)
            continue
        elif not was_active:
            print("  [SMART AUTO-RESUME] Genshin Impact window focused. Auto-skip resumed.")
            was_active = True

        # Check dialogue state in a single pass
        dialogue_active, options_available = get_dialogue_state()

        if not dialogue_active:
            sleep(0.02)
            continue

        # Check if it's time for an occasional break
        if current_time - last_break_check > break_check_interval:
            last_break_check = current_time
            if should_take_break():
                break_duration = take_random_break()
                sleep(break_duration)
                # Reset timing after break
                last_f_press = perf_counter()
                next_f_interval = random_f_key_interval()
                continue

        # Check if it's time to press F
        if current_time - last_f_press >= next_f_interval:
            try:
                if not options_available:
                    press("f")
                else:
                    press(CONFIRM_BUTTON)
            except Exception as e:
                print(f"\n  Error pressing {CONFIRM_BUTTON} key: {e}")

            # Set up next F press timing
            last_f_press = current_time
            next_f_interval = random_f_key_interval()

        # Small sleep to prevent excessive CPU usage
        sleep(0.01)


if __name__ == "__main__":
    Thread(target=main).start()

    with Listener(on_press=on_press) as listener:
        listener.join()
