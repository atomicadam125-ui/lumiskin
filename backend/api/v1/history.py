from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.deps import get_current_user
from db.session import get_db
from models.user import User
from schemas.history import UserHistoryRead
from services.history_service import HistoryService

router = APIRouter()


@router.get("", response_model=UserHistoryRead)
def get_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> UserHistoryRead:
    return HistoryService(db).get_user_history(current_user)
