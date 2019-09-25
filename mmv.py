import ctypes
import time

MOUSEEVENTF_MOVE = 0x0001 # mouse move 
MOUSEEVENTF_ABSOLUTE = MOUSEEVENTF_MOVE + 0x8000 # absolute move 
SM_CXSCREEN = 0
SM_CYSCREEN = 1
POS_MASK = 65536

class Point(ctypes.Structure):
    _fields_ = [("X", ctypes.c_int32), ("Y", ctypes.c_int32)]

    @staticmethod
    def current_position():
        user32 = ctypes.WinDLL("user32")
        user32.GetCursorPos.restype = ctypes.c_bool
        user32.GetCursorPos.argtypes = (ctypes.POINTER(Point),)
        pt = Point()
        user32.GetCursorPos(pt)
        return pt

    def __repr__(self):
        return f"({self.X}, {self.Y})"

def move2(x_delta: int, y_delta: int):
    user32 = ctypes.WinDLL("user32")
    curr_pos = Point.current_position()
    x_abs = POS_MASK * curr_pos.X / user32.GetSystemMetrics(SM_CXSCREEN) + 1 + x_delta
    y_abs = POS_MASK * curr_pos.Y / user32.GetSystemMetrics(SM_CYSCREEN) + 1 + y_delta

    #print(f"current: {curr_pos}, alc:{(x_abs, y_abs)}")
    return user32.mouse_event(MOUSEEVENTF_ABSOLUTE, int(x_abs), int(y_abs), 0, 0)


def move(x_delta: int, y_delta: int):
    user32 = ctypes.WinDLL("user32")
    curr_pos = Point.current_position()
    (x, y) = tuple([max(0,i) for i in [curr_pos.X + x_delta, curr_pos.Y + y_delta]])
    x_abs = POS_MASK * x / user32.GetSystemMetrics(SM_CXSCREEN) + 1
    y_abs = POS_MASK * y / user32.GetSystemMetrics(SM_CYSCREEN) + 1

    print(f"current: {curr_pos}, moved:{(x,y)}, calc:{(x_abs, y_abs)}")
    return user32.mouse_event(MOUSEEVENTF_ABSOLUTE, int(x_abs), int(y_abs), 0, 0)

if __name__ == "__main__":
    delta = 1
    while(1):
        move2(delta, 0)
        delta *= -1
        time.sleep(75)