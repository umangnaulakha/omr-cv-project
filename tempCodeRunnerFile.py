from src.score_sheet import evaluate_sheet, draw_overlay
import json
import cv2

sheet = "data/test/sample1.jpg"

selected, score = evaluate_sheet(sheet, "template.json", "answer_key.json")

print("\nScore:", score)

with open("answer_key.json", "r") as f:
    answer_key = json.load(f)

overlay = draw_overlay(sheet, selected, answer_key, "template.json", "output/graded.png")

cv2.imshow("Graded Sheet", overlay)
cv2.waitKey(0)
cv2.destroyAllWindows()
