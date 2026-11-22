import mediapipe as mp
import numpy as np

from .config import MIN_VISIBILITY
from .geometry import angle, tilt_from_vertical

L = mp.solutions.pose.PoseLandmark

KEY_JOINTS = [L.LEFT_SHOULDER, L.RIGHT_SHOULDER, L.LEFT_HIP, L.RIGHT_HIP,
              L.LEFT_KNEE, L.RIGHT_KNEE, L.LEFT_ANKLE, L.RIGHT_ANKLE]


def key_joints_visible(lm) -> bool:
    return min(lm[j.value].visibility for j in KEY_JOINTS) > MIN_VISIBILITY


def _p(lm, joint):
    p = lm[joint.value]
    return np.array([p.x, p.y])


def extract_features(lm) -> dict:
    """Convert MediaPipe landmarks to the numbers the rules use."""
    sh_l, sh_r = _p(lm, L.LEFT_SHOULDER), _p(lm, L.RIGHT_SHOULDER)
    el_l, el_r = _p(lm, L.LEFT_ELBOW), _p(lm, L.RIGHT_ELBOW)
    wr_l, wr_r = _p(lm, L.LEFT_WRIST), _p(lm, L.RIGHT_WRIST)
    hp_l, hp_r = _p(lm, L.LEFT_HIP), _p(lm, L.RIGHT_HIP)
    kn_l, kn_r = _p(lm, L.LEFT_KNEE), _p(lm, L.RIGHT_KNEE)
    an_l, an_r = _p(lm, L.LEFT_ANKLE), _p(lm, L.RIGHT_ANKLE)

    elbow_l, elbow_r = angle(sh_l, el_l, wr_l), angle(sh_r, el_r, wr_r)
    knee_l, knee_r = angle(hp_l, kn_l, an_l), angle(hp_r, kn_r, an_r)

    torso = (sh_l + sh_r) / 2 - (hp_l + hp_r) / 2
    shoulder_w = np.linalg.norm(sh_l - sh_r) + 1e-9

    return {
        "elbow_min": min(elbow_l, elbow_r),
        "elbow_avg": (elbow_l + elbow_r) / 2,
        "knee_avg": (knee_l + knee_r) / 2,
        "torso_tilt": tilt_from_vertical(torso),
        # image y grows downward, so "above" = smaller y
        "wrists_above_sh": float(np.mean([sh_l[1] - wr_l[1], sh_r[1] - wr_r[1]]) / shoulder_w),
        "ankle_ratio": float(abs(an_l[0] - an_r[0]) / shoulder_w),
    }
