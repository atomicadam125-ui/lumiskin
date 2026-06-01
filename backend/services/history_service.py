from sqlalchemy import select
from sqlalchemy.orm import Session

from models.analysis import Analysis
from models.photo import Photo
from models.questionnaire import Questionnaire
from models.recommendation import Recommendation
from models.user import User
from schemas.history import UserHistoryRead


class HistoryService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_history(self, user: User) -> UserHistoryRead:
        photos = self.db.scalars(
            select(Photo).where(Photo.user_id == user.id).order_by(Photo.created_at.desc())
        )
        questionnaires = self.db.scalars(
            select(Questionnaire)
            .where(Questionnaire.user_id == user.id)
            .order_by(Questionnaire.created_at.desc())
        )
        analyses = self.db.scalars(
            select(Analysis).where(Analysis.user_id == user.id).order_by(Analysis.created_at.desc())
        )
        recommendations = self.db.scalars(
            select(Recommendation)
            .where(Recommendation.user_id == user.id)
            .order_by(Recommendation.created_at.desc())
        )
        return UserHistoryRead(
            photos=list(photos),
            questionnaires=list(questionnaires),
            analyses=list(analyses),
            recommendations=list(recommendations),
        )
