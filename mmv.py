import ctypes
import time

MOUSEEVENTF_MOVE = 0x0001 # mouse move 
user32 = ctypes.WinDLL("user32")

if __name__ == "__main__":
    delta = 1
    while True:
        user32.mouse_event(MOUSEEVENTF_MOVE, delta, 0)
        delta *= -1
        time.sleep(75)