from sqlalchemy.orm import Session

from models.analysis import Analysis
from models.user import User
from schemas.analysis import AnalysisCreate
from services.analysis_service import AnalysisService
from services.image_storage_service import LocalImageStorageService
from services.openai_service import OpenAISkinAnalysisClient


class AnalysisController:
    def __init__(
        self,
        db: Session,
        storage: LocalImageStorageService,
        analyzer: OpenAISkinAnalysisClient,
    ):
        self.service = AnalysisService(db, storage, analyzer)

    def create(self, user: User, payload: AnalysisCreate) -> Analysis:
        return self.service.create(
            user,
            payload.photo_id,
            payload.questionnaire_id,
            photo_ids=payload.photo_ids,
        )

    def list_for_user(self, user: User) -> list[Analysis]:
        return self.service.list_for_user(user)
