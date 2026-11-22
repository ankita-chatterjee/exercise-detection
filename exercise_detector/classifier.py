from collections import deque

import numpy as np

from . import config as C

FEATURES = ["elbow_min", "elbow_avg", "knee_avg",
            "torso_tilt", "wrists_above_sh", "ankle_ratio"]


class ExerciseClassifier:
    """Rule-based: looks at which body parts moved in the window + posture."""

    def __init__(self):
        self.buf = {k: deque(maxlen=C.WINDOW) for k in FEATURES}
        self.votes = deque(maxlen=C.VOTE_WINDOW)

    def update(self, feats: dict) -> str:
        for k in FEATURES:
            self.buf[k].append(feats[k])
        if len(self.buf["knee_avg"]) < C.WINDOW // 2:
            return "detecting..."
        self.votes.append(self._rules())
        return max(set(self.votes), key=self.votes.count)

    def _rng(self, key) -> float:
        return max(self.buf[key]) - min(self.buf[key])

    def _rules(self) -> str:
        elbow_rng = self._rng("elbow_avg")
        knee_rng = self._rng("knee_avg")
        arm_rng = self._rng("wrists_above_sh")
        ankle_rng = self._rng("ankle_ratio")
        tilt = float(np.mean(self.buf["torso_tilt"]))

        # 1. Push-up: horizontal body + bending elbows
        if tilt > C.PUSHUP_TORSO_TILT:
            return "push-up" if elbow_rng > C.PUSHUP_ELBOW_RANGE else "plank/idle"

        # 2. Jumping jack: arms swing overhead AND feet spread/close
        if arm_rng > C.JACK_ARM_RANGE and ankle_rng > C.JACK_ANKLE_RANGE:
            return "jumping jack"

        # 3. Squat: big knee motion, arms mostly still
        if knee_rng > C.SQUAT_KNEE_RANGE and elbow_rng < C.SQUAT_MAX_ELBOW_RANGE:
            return "squat"

        # 4. Bicep curl: big elbow motion, legs still
        if elbow_rng > C.CURL_ELBOW_RANGE and knee_rng < C.CURL_MAX_KNEE_RANGE:
            return "bicep curl"

        return "idle"
