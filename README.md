# Rule-Based Exercise Detection

Detects **squats, push-ups, bicep curls and jumping jacks** from a webcam or video
using MediaPipe Pose landmarks and hand-written rules (no ML classifier), and counts reps.

## Setup
```bash
pip install -r requirements.txt
```

## Run
```bash
python main.py                  # webcam
python main.py --video clip.mp4 # video file
```
Press `q` to quit.

## Structure
| File | Purpose |
|---|---|
| `main.py` | Capture loop / entry point |
| `exercise_detector/config.py` | All thresholds (tune here) |
| `exercise_detector/geometry.py` | Angle and tilt maths |
| `exercise_detector/features.py` | Landmarks -> features |
| `exercise_detector/classifier.py` | Rule-based exercise classifier |
| `exercise_detector/counters.py` | Per-exercise rep counters |
| `exercise_detector/visualizer.py` | On-screen overlay |

## Tips
- Film from the side for squats, push-ups and curls; from the front for jumping jacks.
- Keep the full body in frame.
- Tune thresholds in `config.py` if labels flicker or reps are missed.
