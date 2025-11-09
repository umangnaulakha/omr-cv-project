import cv2
import numpy as np

def detect_candidate_bubbles(thresh):
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    candidates = []

    for c in contours:
        area = cv2.contourArea(c)
        if not (200 < area < 2000):  # bubble size range
            continue

        perimeter = cv2.arcLength(c, True)
        if perimeter == 0:
            continue

        # circularity check
        circularity = 4 * np.pi * (area / (perimeter * perimeter))
        if circularity < 0.6:  # reject text / boxes / weird shapes
            continue

        # bounding box → used to extract bubble interior
        x, y, w, h = cv2.boundingRect(c)
        cx = x + w // 2
        cy = y + h // 2
        r = max(w, h) // 2

        candidates.append((cx, cy, r, c))

    return candidates


def classify_bubble(gray, cx, cy, r):
    # circular mask
    mask = np.zeros_like(gray)
    cv2.circle(mask, (cx, cy), r, 255, -1)

    inside = gray[mask == 255]
    mean_inside = np.mean(inside) / 255.0  # normalized brightness

    # filled bubble is darker → lower mean brightness
    filled = mean_inside < 0.55
    return filled, mean_inside


def visualize(original, bubbles, gray):
    out = original.copy()
    for (cx, cy, r, _) in bubbles:
        filled, _ = classify_bubble(gray, cx, cy, r)
        color = (0, 255, 0) if filled else (0, 0, 255)
        cv2.circle(out, (cx, cy), r, color, 2)
    return out
