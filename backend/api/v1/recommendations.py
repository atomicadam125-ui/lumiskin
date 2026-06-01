from fastapi import APIRouter

from schemas.recommendation_engine import RecommendationEngineResponse, RecommendationInput
from services.recommendation_engine import SkincareRecommendationEngine

router = APIRouter()
engine = SkincareRecommendationEngine()


@router.post("/generate", response_model=RecommendationEngineResponse)
def generate_recommendations(payload: RecommendationInput) -> RecommendationEngineResponse:
    return engine.generate(payload)
