import time


class TickSimulator():
    def __init__(self, fps):
        self.fps = fps
        self.last_update = time.time()

    def simulate(self, obj, callback):
        now = time.time()
        time_delta = 0.0
        frame_duration = 1.0/self.fps
        while self.last_update + time_delta < now:
            callback(obj)
            time_delta += frame_duration
        self.last_update = now