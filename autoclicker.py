import pyautogui
import time
import threading
from pynput import keyboard
# Define the autoclicker class
class AutoClicker:
    def __init__(self):
        self.clicking = False  # Controls the clicking state
        self.delay = 0.1  # Delay between clicks, in seconds

    def start_clicking(self):
        self.clicking = True
        while self.clicking:
            pyautogui.click()
            time.sleep(self.delay)

    def stop_clicking(self):
        self.clicking = False

# Function to listen for keyboard inputs

def on_press(key):
    try:
        if key.char == 's':  # Start clicking when 's' is pressed
            if not clicker_thread.is_alive():
                threading.Thread(target=clicker.start_clicking).start()
        elif key.char == 'e':  # Stop clicking when 'e' is pressed
            clicker.stop_clicking()
    except AttributeError:
        pass

clicker = AutoClicker()
clicker_thread = threading.Thread(target=clicker.start_clicking)

# Set up the listener for keyboard events
with keyboard.Listener(on_press=on_press) as listener:
    print("Press 's' to start clicking and 'e' to stop.")
    listener.join()

