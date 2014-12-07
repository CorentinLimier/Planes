import time


class UserInput():
    has_pressed_left = False
    has_pressed_right = False
    has_pressed_quit = False
    has_pressed_fire = False
    orientation_delta = 0
    speed_delta = 0
    now = None

    def __init__(self):
        self.now = time.time()
        pass