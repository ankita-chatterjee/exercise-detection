from . import config as C


class RepCounter:
    """Base class: hysteresis state machine so jitter isn't double counted."""

    def __init__(self):
        self.count = 0
        self.stage = None

    def update(self, f: dict):
        raise NotImplementedError


class SquatCounter(RepCounter):
    def update(self, f):
        k = f["knee_avg"]
        if k > C.SQUAT_UP:
            if self.stage == "down":
                self.count += 1
            self.stage = "up"
        elif k < C.SQUAT_DOWN:
            self.stage = "down"


class PushUpCounter(RepCounter):
    def update(self, f):
        e = f["elbow_avg"]
        if e > C.PUSHUP_UP:
            if self.stage == "down":
                self.count += 1
            self.stage = "up"
        elif e < C.PUSHUP_DOWN:
            self.stage = "down"


class CurlCounter(RepCounter):
    def update(self, f):
        e = f["elbow_min"]
        if e > C.CURL_DOWN:
            self.stage = "down"
        elif e < C.CURL_UP and self.stage == "down":
            self.stage = "up"
            self.count += 1


class JumpingJackCounter(RepCounter):
    def update(self, f):
        arms_up = f["wrists_above_sh"] > C.JACK_ARMS_UP
        arms_down = f["wrists_above_sh"] < C.JACK_ARMS_DOWN
        feet_open = f["ankle_ratio"] > C.JACK_FEET_OPEN
        feet_closed = f["ankle_ratio"] < C.JACK_FEET_CLOSED
        if arms_up and feet_open:
            self.stage = "open"
        elif arms_down and feet_closed:
            if self.stage == "open":
                self.count += 1
            self.stage = "closed"


COUNTERS = {
    "squat": SquatCounter,
    "push-up": PushUpCounter,
    "bicep curl": CurlCounter,
    "jumping jack": JumpingJackCounter,
}
