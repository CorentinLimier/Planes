import time as system_time


class TickSimulator():
    def __init__(self, fps):
        self.fps = fps
        self.last_update = system_time.time()

    def simulate(self, obj, callback):
        now = system_time.time()
        time_delta = 0.0
        frame_duration = 1.0/self.fps
        while self.last_update + time_delta < now:
            callback(obj)
            time_delta += frame_duration
        self.last_update = now


class IntervalExecutor():
    def __init__(self, time_between_calls_in_second):
        self.time_between_calls_in_second = time_between_calls_in_second
        self.last_execution = system_time.time()

    def execute_if_interval_elapsed(self, obj, callback):
        now = system_time.time()

        if self.last_execution + self.time_between_calls_in_second < now:
            callback(obj)
            self.last_execution = now
