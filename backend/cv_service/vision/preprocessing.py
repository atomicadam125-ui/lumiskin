import cv2
import numpy as np


def normalize_lighting(image_bgr: np.ndarray) -> np.ndarray:
    lab = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2LAB)
    lightness, a_channel, b_channel = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    normalized_l = clahe.apply(lightness)
    normalized_lab = cv2.merge((normalized_l, a_channel, b_channel))
    return cv2.cvtColor(normalized_lab, cv2.COLOR_LAB2BGR)


def skin_mask(image_bgr: np.ndarray) -> np.ndarray:
    ycrcb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2YCrCb)
    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

    ycrcb_mask = cv2.inRange(ycrcb, np.array([0, 133, 77]), np.array([255, 173, 127]))
    hsv_mask = cv2.inRange(hsv, np.array([0, 15, 40]), np.array([35, 255, 255]))
    mask = cv2.bitwise_and(ycrcb_mask, hsv_mask)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    return mask


def quality_score(image_bgr: np.ndarray, mask: np.ndarray, face_confidence: float) -> int:
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    blur = min(1.0, cv2.Laplacian(gray, cv2.CV_64F).var() / 500.0)
    exposure = 1.0 - min(1.0, abs(float(gray.mean()) - 125.0) / 125.0)
    skin_coverage = min(1.0, float(cv2.countNonZero(mask)) / max(1.0, mask.size * 0.45))
    confidence = (0.4 * face_confidence) + (0.25 * blur) + (0.2 * exposure) + (0.15 * skin_coverage)
    return clamp_score(confidence * 100.0)


def clamp_score(value: float) -> int:
    return int(max(0, min(100, round(value))))
