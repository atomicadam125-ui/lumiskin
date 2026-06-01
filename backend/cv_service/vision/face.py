from dataclasses import dataclass

import cv2
import mediapipe as mp
import numpy as np

from cv_service.core.config import settings


@dataclass(frozen=True)
class FaceGeometry:
    bbox: tuple[int, int, int, int]
    landmarks: dict[str, tuple[int, int]]
    confidence: float


class FaceProcessor:
    def __init__(self) -> None:
        self._face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=settings.max_faces,
            refine_landmarks=True,
            min_detection_confidence=settings.min_face_confidence,
        )

    def extract_geometry(self, image_bgr: np.ndarray) -> FaceGeometry:
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        result = self._face_mesh.process(image_rgb)
        if not result.multi_face_landmarks:
            raise ValueError("No face detected")

        landmarks = result.multi_face_landmarks[0].landmark
        height, width = image_bgr.shape[:2]
        points = np.array([(int(point.x * width), int(point.y * height)) for point in landmarks])

        x, y, w, h = cv2.boundingRect(points)
        named = {
            "left_eye": self._mean_point(points, [33, 133, 159, 145]),
            "right_eye": self._mean_point(points, [362, 263, 386, 374]),
            "nose_tip": tuple(points[1]),
            "mouth_center": self._mean_point(points, [13, 14]),
            "chin": tuple(points[152]),
            "forehead": tuple(points[10]),
            "left_cheek": tuple(points[234]),
            "right_cheek": tuple(points[454]),
        }
        confidence = min(1.0, max(0.0, (w * h) / float(width * height) * 6.0))
        return FaceGeometry(bbox=(x, y, w, h), landmarks=named, confidence=confidence)

    def align_face(self, image_bgr: np.ndarray, geometry: FaceGeometry) -> np.ndarray:
        left_eye = np.array(geometry.landmarks["left_eye"], dtype=np.float32)
        right_eye = np.array(geometry.landmarks["right_eye"], dtype=np.float32)
        eye_center = (left_eye + right_eye) / 2.0
        delta = right_eye - left_eye
        angle = np.degrees(np.arctan2(delta[1], delta[0]))

        rotation = cv2.getRotationMatrix2D(tuple(eye_center), angle, 1.0)
        aligned = cv2.warpAffine(
            image_bgr,
            rotation,
            (image_bgr.shape[1], image_bgr.shape[0]),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_REPLICATE,
        )

        x, y, w, h = geometry.bbox
        pad = int(max(w, h) * 0.18)
        x0 = max(0, x - pad)
        y0 = max(0, y - pad)
        x1 = min(aligned.shape[1], x + w + pad)
        y1 = min(aligned.shape[0], y + h + pad)
        return aligned[y0:y1, x0:x1]

    @staticmethod
    def _mean_point(points: np.ndarray, indexes: list[int]) -> tuple[int, int]:
        point = points[indexes].mean(axis=0)
        return int(point[0]), int(point[1])
