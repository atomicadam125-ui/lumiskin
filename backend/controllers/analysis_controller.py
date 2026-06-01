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
        storage: LocalImageStorageService | None = None,
        analyzer: OpenAISkinAnalysisClient | None = None,
    ):
        self.db = db
        self.storage = storage
        self.analyzer = analyzer

    def create(self, user: User, payload: AnalysisCreate) -> Analysis:
        if self.storage is None or self.analyzer is None:
            raise RuntimeError("Analysis creation requires storage and analyzer services")
        return AnalysisService(self.db, self.storage, self.analyzer).create(
            user,
            payload.photo_id,
            payload.questionnaire_id,
            photo_ids=payload.photo_ids,
        )

    def list_for_user(self, user: User) -> list[Analysis]:
        return AnalysisService.list_for_user(self.db, user)
