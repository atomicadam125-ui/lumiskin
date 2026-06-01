from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.deps import get_current_user, get_storage_service
from db.session import get_db
from models.user import User
from schemas.auth import AppleLoginRequest, LoginRequest, RegisterRequest, TokenResponse
from schemas.user import UserRead
from services.auth_service import AuthService
from services.image_storage_service import LocalImageStorageService

router = APIRouter()


@router.post("/register", response_model=UserRead, status_code=201)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> User:
    return AuthService(db).register(payload)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    return AuthService(db).login(payload.email, payload.password)


@router.post("/apple", response_model=TokenResponse)
def login_with_apple(payload: AppleLoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    return AuthService(db).login_with_apple(payload)


@router.get("/me", response_model=UserRead)
def me(current_user: User = Depends(get_current_user)) -> User:
    return current_user


@router.delete("/me", status_code=204)
def delete_me(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    storage: LocalImageStorageService = Depends(get_storage_service),
) -> None:
    AuthService(db).delete_account(current_user, storage)
