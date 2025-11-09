import cv2
import numpy as np


def preprocess_image(image_path, apply_clahe=True, debug=False):
    """
    Preprocess OMR sheet image:
    1. Read image
    2. Convert to grayscale
    3. Apply Gaussian blur
    4. (Optional) Apply CLAHE for illumination normalization
    5. Apply adaptive thresholding

    Returns:
        gray (ndarray): grayscale image
        thresh (ndarray): adaptive thresholded binary image
    """

    # 1. Load image
    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(f"Could not read image at path: {image_path}")

    # 2. Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 3. Gaussian blur (reduces noise that interferes with thresholding)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 4. CLAHE for contrast normalization (helps under uneven lighting)
    if apply_clahe:
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(blurred)
    else:
        enhanced = blurred

    # 5. Adaptive thresholding (binary image separating marks from background)
    thresh = cv2.adaptiveThreshold(
        enhanced,
        maxValue=255,
        adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        thresholdType=cv2.THRESH_BINARY_INV,
        blockSize=25,     # neighborhood window size
        C=15              # constant subtracted from mean
    )

    if debug:
        cv2.imshow("Original", image)
        cv2.imshow("Grayscale", gray)
        cv2.imshow("After CLAHE", enhanced)
        cv2.imshow("Adaptive Threshold", thresh)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return gray, thresh
