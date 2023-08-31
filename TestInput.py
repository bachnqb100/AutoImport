import keyboard
import pyautogui

# Define the hotkey combination (you can customize this)
HOTKEY = "f7"

def get_mouse_position():
    x, y = pyautogui.position()
    print(f"Mouse Position: x={x}, y={y}")

# Register the hotkey
keyboard.add_hotkey(HOTKEY, get_mouse_position)

print(f"Press {HOTKEY} to get mouse position. Press 'Ctrl+C' to exit.")

# Keep the script running
keyboard.wait("esc")
