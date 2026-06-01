from fastapi import HTTPException, status

from cv_service.vision.face import FaceProcessor
from cv_service.vision.features import SkinFeatureScorer
from cv_service.vision.image_io import decode_image, resize_for_inference
from cv_service.vision.preprocessing import normalize_lighting, quality_score, skin_mask
from cv_service.vision.regions import extract_regions


class SkincareAnalysisPipeline:
    def __init__(self) -> None:
        self.face_processor = FaceProcessor()
        self.feature_scorer = SkinFeatureScorer()

    def analyze(self, image_bytes: bytes) -> dict[str, int]:
        try:
            image = resize_for_inference(decode_image(image_bytes))
            geometry = self.face_processor.extract_geometry(image)
            aligned_face = self.face_processor.align_face(image, geometry)
            normalized_face = normalize_lighting(aligned_face)
            mask = skin_mask(normalized_face)
            regions = extract_regions(normalized_face)
            scores = self.feature_scorer.score(regions, mask)
            scores["confidence"] = quality_score(normalized_face, mask, geometry.confidence)
            return scores
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)
            ) from exc
