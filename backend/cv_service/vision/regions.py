from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class FaceRegions:
    full_face: np.ndarray
    forehead: np.ndarray
    cheeks: np.ndarray
    nose: np.ndarray
    eye_area: np.ndarray


def extract_regions(face_bgr: np.ndarray) -> FaceRegions:
    height, width = face_bgr.shape[:2]

    forehead = face_bgr[
        int(height * 0.08) : int(height * 0.32), int(width * 0.25) : int(width * 0.75)
    ]
    left_cheek = face_bgr[
        int(height * 0.38) : int(height * 0.72), int(width * 0.08) : int(width * 0.42)
    ]
    right_cheek = face_bgr[
        int(height * 0.38) : int(height * 0.72), int(width * 0.58) : int(width * 0.92)
    ]
    cheeks = np.concatenate((left_cheek, right_cheek), axis=1)
    nose = face_bgr[int(height * 0.32) : int(height * 0.68), int(width * 0.38) : int(width * 0.62)]
    eye_area = face_bgr[
        int(height * 0.22) : int(height * 0.42), int(width * 0.12) : int(width * 0.88)
    ]

    return FaceRegions(
        full_face=face_bgr,
        forehead=forehead,
        cheeks=cheeks,
        nose=nose,
        eye_area=eye_area,
    )
