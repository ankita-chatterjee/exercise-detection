"""All tunable thresholds live here."""

# --- general ---
WINDOW = 45              # frames of history used for motion statistics (~1.5 s @ 30 fps)
VOTE_WINDOW = 15         # majority-vote smoothing of the label
MIN_VISIBILITY = 0.5     # skip frames where key joints are less visible than this

# --- classification rules (ranges are max - min over WINDOW) ---
PUSHUP_TORSO_TILT = 55       # deg from vertical => body is horizontal
PUSHUP_ELBOW_RANGE = 25

JACK_ARM_RANGE = 0.8         # wrist height vs shoulder, in shoulder-widths
JACK_ANKLE_RANGE = 0.6       # ankle spread, in shoulder-widths

SQUAT_KNEE_RANGE = 40
SQUAT_MAX_ELBOW_RANGE = 40

CURL_ELBOW_RANGE = 50
CURL_MAX_KNEE_RANGE = 20

# --- rep counting (hysteresis thresholds) ---
SQUAT_DOWN, SQUAT_UP = 100, 160          # knee angle
PUSHUP_DOWN, PUSHUP_UP = 90, 160         # elbow angle
CURL_UP, CURL_DOWN = 50, 150             # elbow angle (min of both arms)

JACK_ARMS_UP, JACK_ARMS_DOWN = 0.3, -0.3 # wrist-vs-shoulder height
JACK_FEET_OPEN, JACK_FEET_CLOSED = 1.6, 1.2
