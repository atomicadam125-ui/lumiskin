from sqlalchemy.orm import Session

from models.questionnaire import Questionnaire
from models.user import User
from schemas.questionnaire import QuestionnaireCreate


class QuestionnaireService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User, payload: QuestionnaireCreate) -> Questionnaire:
        questionnaire = Questionnaire(user_id=user.id, **payload.model_dump())
        self.db.add(questionnaire)
        self.db.commit()
        self.db.refresh(questionnaire)
        return questionnaire
