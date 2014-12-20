import time


class UserInput():
    has_pressed_left = False
    has_pressed_right = False
    has_pressed_quit = False
    has_pressed_fire = False
    now = None

    def __init__(self):
        self.now = time.time()
        pass

    def has_pressed_something(self):
        return self.has_pressed_left or self.has_pressed_right or self.has_pressed_fire


class UserInputAggregate():
    pressed_left_frame_count = 0
    pressed_right_frame_count = 0
    now = None

    def __init__(self):
        self.now = time.time()
        pass

    def has_pressed_something(self):
        return self.pressed_left_frame_count > 0 or self.pressed_right_frame_count > 0
