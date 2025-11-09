import cv2
import json
import numpy as np


def load_template(template_path="template.json"):
    with open(template_path, "r") as f:
        return json.load(f)


def load_answer_key(key_path="answer_key.json"):
    with open(key_path, "r") as f:
        return json.load(f)


def compute_fill(gray, x, y, r, inner_scale=0.80):
    """
    Compute fill intensity using only the inner portion of the bubble (ignore outline).
    Lower mean intensity = darker = filled.
    inner_scale controls how much of radius to use: 0.75–0.90 recommended.
    """
    mask = np.zeros_like(gray, dtype=np.uint8)
    inner_r = max(1, int(r * inner_scale))  # shrink ROI to avoid outline
    cv2.circle(mask, (x, y), inner_r, 255, -1)
    inside = gray[mask == 255]

    # Normalized darkness score (0=white, 1=solid black)
    return 1.0 - (np.mean(inside) / 255.0)

def classify_row(fills, min_fill=0.32, margin=0.06):
    """
    fills is dict: {"A": 0.12, "B": 0.65, "C": 0.18, "D": 0.11}
    Returns chosen option or "BLANK" or "AMBIG"
    """
    sorted_opts = sorted(fills.items(), key=lambda x: x[1], reverse=True)
    top_opt, top_val = sorted_opts[0]
    second_val = sorted_opts[1][1]

    # If strongest bubble not dark enough → blank
    if top_val < min_fill:
        return "BLANK"

    # If two bubbles are close → ambiguous
    if (top_val - second_val) < margin:
        return "AMBIG"

    return top_opt


def evaluate_sheet(image_path, template_path="../template.json", answer_key_path=None):
    template = load_template(template_path)
    gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    selected_answers = {}

    for q, opts in template.items():
        best_opt = None
        best_fill = -1

        for opt, (x, y, r) in opts.items():
            fill = compute_fill(gray, x, y, r)
            if fill > best_fill:
                best_fill = fill
                best_opt = opt

        selected_answers[q] = best_opt

    score = None
    if answer_key_path:
        answer_key = load_answer_key(answer_key_path)
        score = sum(selected_answers[q] == answer_key[q] for q in answer_key)

    return selected_answers, score

def draw_overlay(image_path, selected_answers, answer_key, template_path="../template.json", output_path="output/graded.png"):
    import cv2, json

    with open(template_path, "r") as f:
        template = json.load(f)

    img = cv2.imread(image_path)

    for q, opts in template.items():
        correct = answer_key[q]
        student = selected_answers[q]

        for opt, (x, y, r) in opts.items():
            x, y, r = int(x), int(y), int(r)

            # Case 1: Student filled correctly
            if student == correct and opt == student:
                cv2.circle(img, (x, y), r, (0, 255, 0), 3)  # GREEN bold

            # Case 2: Student filled wrong
            elif student != "BLANK" and student != "AMBIG" and opt == student and student != correct:
                cv2.circle(img, (x, y), r, (0, 0, 255), 3)  # RED bold

            # Case 3: Student left blank → show only the correct bubble
            elif student == "BLANK" and opt == correct:
                cv2.circle(img, (x, y), r, (0, 255, 0), 2)  # Green thin

            # Case 4: Ambiguous fill (multiple choices)
            elif student == "AMBIG" and opt == correct:
                cv2.circle(img, (x, y), r, (0, 255, 255), 3)  # YELLOW bold

            # otherwise → draw nothing

    cv2.imwrite(output_path, img)
    return img
