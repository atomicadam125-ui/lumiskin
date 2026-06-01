from fastapi import APIRouter, File, HTTPException, UploadFile, status

from cv_service.core.config import settings
from cv_service.models.schemas import SkinAnalysisResponse
from cv_service.vision.pipeline import SkincareAnalysisPipeline

router = APIRouter(tags=["analysis"])
pipeline: SkincareAnalysisPipeline | None = None

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}


def get_pipeline() -> SkincareAnalysisPipeline:
    global pipeline
    if pipeline is None:
        pipeline = SkincareAnalysisPipeline()
    return pipeline


@router.post("/analyze", response_model=SkinAnalysisResponse)
async def analyze_selfie(file: UploadFile = File(...)) -> SkinAnalysisResponse:
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Only JPEG, PNG, and WebP images are supported",
        )

    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Image is empty")
    if len(image_bytes) > settings.max_image_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="Image is too large"
        )

    result = get_pipeline().analyze(image_bytes)
    return SkinAnalysisResponse(**result)
