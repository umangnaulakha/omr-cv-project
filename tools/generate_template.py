import json

with open("ref_points.json", "r") as f:
    (Q1A, Q1B, Q2A, Q16A) = [tuple(p) for p in json.load(f)]

dx = Q1B[0] - Q1A[0]        # horizontal spacing between choices
dy = Q2A[1] - Q1A[1]        # vertical spacing between questions
col_dx = Q16A[0] - Q1A[0]   # spacing between columns
r = 18                      # approximate bubble radius (adjust if needed)

TEMPLATE = {}
col_starts = [0, col_dx, col_dx*2, col_dx*3]

q = 1
for col_offset in col_starts:
    for row in range(15):  # 15 questions per column
        y = Q1A[1] + row * dy
        TEMPLATE[f"Q{q}"] = {
            "A": [Q1A[0] + col_offset, y, r],
            "B": [Q1A[0] + col_offset + dx, y, r],
            "C": [Q1A[0] + col_offset + 2*dx, y, r],
            "D": [Q1A[0] + col_offset + 3*dx, y, r],
        }
        q += 1

with open("template.json", "w") as f:
    json.dump(TEMPLATE, f, indent=2)

print("✅ template.json generated successfully!")

