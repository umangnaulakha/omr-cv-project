import cv2
import json

points = []

def click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        print(f"Captured: {(x, y)}")

img = cv2.imread("../data/template.jpg")
cv2.imshow("Click: Q1-A, Q1-B, Q2-A, Q16-A (IN THIS ORDER)", img)
cv2.setMouseCallback("Click: Q1-A, Q1-B, Q2-A, Q16-A (IN THIS ORDER)", click)

print("\nINSTRUCTIONS:")
print("1) Click CENTER of Q1-A")
print("2) Click CENTER of Q1-B")
print("3) Click CENTER of Q2-A")
print("4) Click CENTER of Q16-A")
print("5) Press Q to save\n")

while True:
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cv2.destroyAllWindows()

with open("ref_points.json", "w") as f:
    json.dump(points, f, indent=2)

print("\nSaved → ref_points.json")
