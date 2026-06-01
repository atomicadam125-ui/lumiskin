import cv2
import numpy as np


def decode_image(image_bytes: bytes) -> np.ndarray:
    buffer = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(buffer, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Could not decode image")
    return image


def resize_for_inference(image: np.ndarray, max_side: int = 1280) -> np.ndarray:
    height, width = image.shape[:2]
    longest = max(height, width)
    if longest <= max_side:
        return image

    scale = max_side / float(longest)
    size = (int(width * scale), int(height * scale))
    return cv2.resize(image, size, interpolation=cv2.INTER_AREA)
