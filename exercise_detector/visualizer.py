import cv2


def draw_overlay(frame, label, counters):
    h = 60 + 24 * len(counters)
    cv2.rectangle(frame, (0, 0), (330, h), (30, 30, 30), -1)
    cv2.putText(frame, f"Exercise: {label}", (10, 28),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    for i, (name, c) in enumerate(counters.items()):
        cv2.putText(frame, f"{name}: {c.count}", (10, 58 + 24 * i),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    return frame
