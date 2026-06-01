import cv2
import numpy as np

from cv_service.vision.preprocessing import clamp_score
from cv_service.vision.regions import FaceRegions
from cv_service.vision.torch_features import TorchTextureExtractor


class SkinFeatureScorer:
    def __init__(self) -> None:
        self.torch_texture = TorchTextureExtractor()

    def score(self, regions: FaceRegions, mask: np.ndarray) -> dict[str, int]:
        return {
            "acne_score": self._acne_score(regions.cheeks, mask),
            "redness_score": self._redness_score(regions.full_face, mask),
            "pigmentation_score": self._pigmentation_score(regions.full_face, mask),
            "wrinkle_score": self._wrinkle_score(regions.eye_area, regions.forehead),
            "oiliness_score": self._oiliness_score(regions.forehead, regions.nose),
            "dryness_score": self._dryness_score(regions.cheeks, mask),
        }

    def _acne_score(self, image_bgr: np.ndarray, _: np.ndarray) -> int:
        lab = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2LAB)
        _, a_channel, _ = cv2.split(lab)
        enhanced = cv2.GaussianBlur(a_channel, (0, 0), 2)
        spots = cv2.inRange(enhanced, 150, 255)
        spots = cv2.morphologyEx(spots, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        contours, _ = cv2.findContours(spots, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        lesion_like = [
            cv2.contourArea(contour) for contour in contours if 8 <= cv2.contourArea(contour) <= 600
        ]
        density = sum(lesion_like) / max(1.0, image_bgr.shape[0] * image_bgr.shape[1])
        return clamp_score(density * 2200.0)

    def _redness_score(self, image_bgr: np.ndarray, mask: np.ndarray) -> int:
        lab = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2LAB)
        _, a_channel, _ = cv2.split(lab)
        skin_pixels = a_channel[mask > 0]
        if skin_pixels.size == 0:
            return 0
        redness = max(0.0, float(skin_pixels.mean()) - 132.0)
        spread = float(skin_pixels.std())
        return clamp_score((redness * 4.0) + (spread * 1.5))

    def _pigmentation_score(self, image_bgr: np.ndarray, mask: np.ndarray) -> int:
        lab = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2LAB)
        lightness, _, _ = cv2.split(lab)
        skin_pixels = lightness[mask > 0]
        if skin_pixels.size == 0:
            return 0
        unevenness = float(np.percentile(skin_pixels, 90) - np.percentile(skin_pixels, 10))
        dark_pixel_ratio = float(np.mean(skin_pixels < np.percentile(skin_pixels, 25)))
        return clamp_score((unevenness * 1.3) + (dark_pixel_ratio * 40.0))

    def _wrinkle_score(self, eye_area_bgr: np.ndarray, forehead_bgr: np.ndarray) -> int:
        texture_score = self._line_texture_score(eye_area_bgr)
        forehead_score = self._line_texture_score(forehead_bgr)
        return clamp_score((texture_score * 0.65) + (forehead_score * 0.35))

    def _oiliness_score(self, forehead_bgr: np.ndarray, nose_bgr: np.ndarray) -> int:
        forehead_shine = self._specular_ratio(forehead_bgr)
        nose_shine = self._specular_ratio(nose_bgr)
        return clamp_score(((forehead_shine * 0.45) + (nose_shine * 0.55)) * 240.0)

    def _dryness_score(self, image_bgr: np.ndarray, mask: np.ndarray) -> int:
        gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
        torch_features = self.torch_texture.extract(gray)
        saturation = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)[:, :, 1]
        region_mask = cv2.resize(mask, (saturation.shape[1], saturation.shape[0]))
        skin_saturation = saturation[region_mask > 0]
        low_saturation = (
            0.0 if skin_saturation.size == 0 else max(0.0, 80.0 - float(skin_saturation.mean()))
        )
        return clamp_score((torch_features["edge_mean"] * 120.0) + (low_saturation * 0.45))

    def _line_texture_score(self, image_bgr: np.ndarray) -> float:
        gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
        blackhat_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (11, 3))
        blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, blackhat_kernel)
        return min(100.0, float(np.percentile(blackhat, 95)) * 2.5)

    def _specular_ratio(self, image_bgr: np.ndarray) -> float:
        hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
        saturation = hsv[:, :, 1]
        value = hsv[:, :, 2]
        highlights = (value > 205) & (saturation < 70)
        return float(np.mean(highlights))
