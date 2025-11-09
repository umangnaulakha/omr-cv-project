import cv2
import numpy as np

def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    d = np.diff(pts, axis=1)

    rect[0] = pts[np.argmin(s)]      # top-left
    rect[2] = pts[np.argmax(s)]      # bottom-right
    rect[1] = pts[np.argmin(d)]      # top-right
    rect[3] = pts[np.argmax(d)]      # bottom-left

    return rect


def detect_fiducials(original):
    """
    Detects 4 black fiducial squares on the OMR sheet.
    Works on original image (not threshold).
    """
    gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)

    # Regular threshold: black stays black, white becomes white
    _, bin_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    contours, _ = cv2.findContours(bin_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    centers = []

    for c in contours:
        area = cv2.contourArea(c)

        # Adjust these based on your sheet (we will tune if needed)
        if 300 < area < 3000:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)

            # Only take perfect-ish squares
            if len(approx) == 4:
                M = cv2.moments(c)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    centers.append((cx, cy))

    if len(centers) != 4:
        raise ValueError(f"Expected 4 fiducials, found {len(centers)} — adjust area limits.")

    return np.array(centers, dtype="float32")



def align_document(original, thresh, output_size=(2000, 2800), debug=False):
    """
    Align sheet using 4 fiducial markers.
    output_size: width, height of the canonical sheet
    """

    # STEP 1: detect fiducial center points
    pts = detect_fiducials(thresh)
    pts = order_points(pts)

    # STEP 2: define target layout coordinates in canonical sheet
    (W, H) = output_size
    dst = np.array([
        [100, 100],       # TL position in aligned image
        [W-100, 100],     # TR
        [W-100, H-100],   # BR
        [100, H-100]      # BL
    ], dtype="float32")

    # STEP 3: compute homography + warp image
    Hmat = cv2.getPerspectiveTransform(pts, dst)
    warped = cv2.warpPerspective(original, Hmat, (W, H))

    if debug:
        dbg = original.copy()
        for (x, y) in pts:
            cv2.circle(dbg, (int(x), int(y)), 12, (0, 0, 255), -1)
        cv2.imshow("Detected Fiducials", dbg)
        cv2.imshow("Aligned Sheet", warped)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return warped
