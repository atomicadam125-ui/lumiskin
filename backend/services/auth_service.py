from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.security import create_access_token, hash_password, verify_password
from models.user import User
from schemas.auth import AppleLoginRequest, RegisterRequest, TokenResponse
from services.apple_auth_service import AppleIdentityVerifier


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register(self, payload: RegisterRequest) -> User:
        existing = self.db.scalar(select(User).where(User.email == payload.email.lower()))
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
            )

        user = User(
            email=payload.email.lower(),
            password_hash=hash_password(payload.password),
            full_name=payload.full_name,
            auth_provider="password",
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def login(self, email: str, password: str) -> TokenResponse:
        user = self.db.scalar(select(User).where(User.email == email.lower()))
        if (
            user is None
            or not user.is_active
            or user.password_hash is None
            or not verify_password(password, user.password_hash)
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
            )

        return TokenResponse(access_token=create_access_token(str(user.id)))

    def login_with_apple(self, payload: AppleLoginRequest) -> TokenResponse:
        claims = AppleIdentityVerifier().verify(payload.identity_token)
        apple_sub = claims["sub"]
        email = claims.get("email")

        user = self.db.scalar(select(User).where(User.apple_sub == apple_sub))
        if user is None and email:
            user = self.db.scalar(select(User).where(User.email == email.lower()))

        if user is None:
            if not email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Apple account did not provide an email address",
                )
            user = User(
                email=email.lower(),
                full_name=payload.full_name,
                auth_provider="apple",
                apple_sub=apple_sub,
            )
            self.db.add(user)
        else:
            user.apple_sub = user.apple_sub or apple_sub
            user.auth_provider = "apple" if user.password_hash is None else user.auth_provider
            user.is_active = True
            user.deleted_at = None
            if payload.full_name and not user.full_name:
                user.full_name = payload.full_name

        self.db.commit()
        self.db.refresh(user)
        return TokenResponse(access_token=create_access_token(str(user.id)))

    def delete_account(self, user: User, storage: object | None = None) -> None:
        if storage is not None and hasattr(storage, "delete_user_images"):
            storage.delete_user_images(user.id)
        self.db.delete(user)
        self.db.commit()
