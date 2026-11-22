"""Entry point.  python main.py [--video path]   (press 'q' to quit)"""
import argparse

import cv2
import mediapipe as mp

from exercise_detector import (COUNTERS, ExerciseClassifier,
                               extract_features, key_joints_visible)
from exercise_detector.visualizer import draw_overlay

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", default=None, help="video file (default: webcam)")
    args = ap.parse_args()

    cap = cv2.VideoCapture(args.video if args.video else 0)
    classifier = ExerciseClassifier()
    counters = {name: cls() for name, cls in COUNTERS.items()}
    label = "detecting..."

    with mp_pose.Pose(min_detection_confidence=0.5,
                      min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ok, frame = cap.read()
            if not ok:
                break

            res = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if res.pose_landmarks:
                lm = res.pose_landmarks.landmark
                if key_joints_visible(lm):
                    feats = extract_features(lm)
                    label = classifier.update(feats)
                    if label in counters:
                        counters[label].update(feats)
                mp_draw.draw_landmarks(frame, res.pose_landmarks,
                                       mp_pose.POSE_CONNECTIONS)

            cv2.imshow("Exercise detection", draw_overlay(frame, label, counters))
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
