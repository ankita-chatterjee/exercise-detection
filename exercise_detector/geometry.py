import numpy as np


def angle(a, b, c) -> float:
    """Angle ABC in degrees, vertex at b."""
    ba, bc = a - b, c - b
    cosv = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-9)
    return float(np.degrees(np.arccos(np.clip(cosv, -1.0, 1.0))))


def tilt_from_vertical(vec) -> float:
    """0 = vertical vector, 90 = horizontal vector."""
    return float(np.degrees(np.arctan2(abs(vec[0]), abs(vec[1]) + 1e-9)))
