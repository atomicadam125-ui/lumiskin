from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.deps import get_current_user, get_recommendation_client
from db.session import get_db
from models.analysis import Analysis
from models.recommendation import Recommendation
from models.user import User
from schemas.analysis import AnalysisCreate, AnalysisRead
from schemas.recommendation import RecommendationRead
from services.analysis_service import AnalysisService
from services.openai_service import OpenAIRecommendationClient
from services.recommendation_service import RecommendationService

router = APIRouter()


@router.post("", response_model=AnalysisRead, status_code=201)
def create_analysis(
    payload: AnalysisCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Analysis:
    return AnalysisService(db).create(
        current_user,
        payload.photo_id,
        payload.questionnaire_id,
        photo_ids=payload.photo_ids,
        scores=payload.scores,
        model_versions=payload.model_versions,
    )


@router.get("", response_model=list[AnalysisRead])
def list_analyses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[Analysis]:
    return AnalysisService(db).list_for_user(current_user)


@router.post("/{analysis_id}/recommendations", response_model=RecommendationRead, status_code=201)
def create_recommendation(
    analysis_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    llm: OpenAIRecommendationClient = Depends(get_recommendation_client),
) -> Recommendation:
    return RecommendationService(db, llm).create_for_analysis(current_user, analysis_id)
