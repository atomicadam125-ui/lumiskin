from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.config import settings
from core.security import decode_token
from db.session import get_db
from models.user import User
from services.image_storage_service import LocalImageStorageService
from services.openai_service import OpenAIRecommendationClient, OpenAISkinAnalysisClient

DEV_AUTH_TOKEN = "local-dev-bypass"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


def get_current_user(
    token: str | None = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    if settings.environment == "local" and token == DEV_AUTH_TOKEN:
        return get_or_create_local_dev_user(db)

    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise credentials_error

    try:
        payload = decode_token(token)
        user_id = UUID(payload["sub"])
    except (KeyError, TypeError, ValueError):
        raise credentials_error from None

    user = db.get(User, user_id)
    if user is None or not user.is_active:
        raise credentials_error
    return user


def get_or_create_local_dev_user(db: Session) -> User:
    email = "local-dev@lumiskin.test"
    user = db.scalar(select(User).where(User.email == email))
    if user is not None:
        return user

    user = User(
        email=email,
        full_name="Local Dev",
        auth_provider="local-dev",
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_storage_service() -> LocalImageStorageService:
    return LocalImageStorageService()


def get_recommendation_client() -> OpenAIRecommendationClient:
    return OpenAIRecommendationClient()


def get_skin_analysis_client() -> OpenAISkinAnalysisClient:
    return OpenAISkinAnalysisClient()
