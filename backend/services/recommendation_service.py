from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from core.config import settings
from models.analysis import Analysis
from models.recommendation import Recommendation
from models.user import User
from services.openai_service import PROMPT_VERSION, OpenAIRecommendationClient


class RecommendationService:
    def __init__(self, db: Session, llm: OpenAIRecommendationClient):
        self.db = db
        self.llm = llm

    def create_for_analysis(self, user: User, analysis_id: UUID) -> Recommendation:
        analysis = self.db.get(Analysis, analysis_id)
        if analysis is None or analysis.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not found")

        questionnaire_payload = None
        if analysis.questionnaire is not None:
            questionnaire_payload = {
                "skin_type": analysis.questionnaire.skin_type,
                "sensitivity_level": analysis.questionnaire.sensitivity_level,
                "acne_frequency": analysis.questionnaire.acne_frequency,
                "current_products": analysis.questionnaire.current_products,
                "allergies": analysis.questionnaire.allergies,
            }

        generated = self.llm.generate(analysis.skin_profile, questionnaire_payload)
        recommendation = Recommendation(
            user_id=user.id,
            analysis_id=analysis.id,
            routine=generated,
            explanation=generated.get("explanation"),
            llm_model=settings.openai_model,
            prompt_version=PROMPT_VERSION,
        )
        self.db.add(recommendation)
        self.db.commit()
        self.db.refresh(recommendation)
        return recommendation
