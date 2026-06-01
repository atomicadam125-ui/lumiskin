from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.deps import get_current_user
from db.session import get_db
from models.questionnaire import Questionnaire
from models.user import User
from schemas.questionnaire import QuestionnaireCreate, QuestionnaireRead
from services.questionnaire_service import QuestionnaireService

router = APIRouter()


@router.post("", response_model=QuestionnaireRead, status_code=201)
def create_questionnaire(
    payload: QuestionnaireCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Questionnaire:
    return QuestionnaireService(db).create(current_user, payload)
