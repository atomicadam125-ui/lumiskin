from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.deps import (
    get_current_user,
    get_recommendation_client,
    get_skin_analysis_client,
    get_storage_service,
)
from controllers.analysis_controller import AnalysisController
from db.session import get_db
from models.analysis import Analysis
from models.recommendation import Recommendation
from models.user import User
from schemas.analysis import AnalysisCreate, AnalysisRead
from schemas.recommendation import RecommendationRead
from services.image_storage_service import LocalImageStorageService
from services.openai_service import OpenAIRecommendationClient, OpenAISkinAnalysisClient
from services.recommendation_service import RecommendationService

router = APIRouter()


@router.post("", response_model=AnalysisRead, status_code=201)
def create_analysis(
    payload: AnalysisCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    storage: LocalImageStorageService = Depends(get_storage_service),
    analyzer: OpenAISkinAnalysisClient = Depends(get_skin_analysis_client),
) -> Analysis:
    return AnalysisController(db, storage, analyzer).create(current_user, payload)


@router.get("", response_model=list[AnalysisRead])
def list_analyses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[Analysis]:
    return AnalysisController(db).list_for_user(current_user)


@router.post("/{analysis_id}/recommendations", response_model=RecommendationRead, status_code=201)
def create_recommendation(
    analysis_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    llm: OpenAIRecommendationClient = Depends(get_recommendation_client),
) -> Recommendation:
    return RecommendationService(db, llm).create_for_analysis(current_user, analysis_id)
