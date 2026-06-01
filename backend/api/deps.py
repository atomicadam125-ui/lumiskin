from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from core.security import decode_token
from db.session import get_db
from models.user import User
from services.openai_service import OpenAIRecommendationClient
from services.s3_service import S3StorageService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        user_id = UUID(payload["sub"])
    except (KeyError, TypeError, ValueError):
        raise credentials_error from None

    user = db.get(User, user_id)
    if user is None or not user.is_active:
        raise credentials_error
    return user


def get_storage_service() -> S3StorageService:
    return S3StorageService()


def get_recommendation_client() -> OpenAIRecommendationClient:
    return OpenAIRecommendationClient()
