import pyautogui
import time
import keyboard

def auto_clicker(x, y, interval):
    """
    Automatically clicks at the given screen coordinates (x, y) at specified intervals.

    :param x: X-coordinate of the click position
    :param y: Y-coordinate of the click position
    :param interval: Time in seconds between clicks
    """
    print(f"Auto-clicker started. Clicking at ({x}, {y}) every {interval} seconds.")
    print("Press 'q' to stop.")
    while True:
        # Check if 'q' is pressed to exit the loop
        if keyboard.is_pressed('q'):
            print("\nStopping auto-clicker.")
            break
        pyautogui.click(x, y)
        time.sleep(interval)

if __name__ == "__main__":
    # Set your desired coordinates and interval
    click_x = 1292  # Replace with your desired X-coordinate
    click_y = 709  # Replace with your desired Y-coordinate
    click_interval = 0.05  # Time in seconds between clicks
    
    # Start the auto-clicker
    auto_clicker(click_x, click_y, click_interval)

