from datetime import UTC, datetime, timedelta
from typing import Any

from jose import JWTError, jwt
from pwdlib import PasswordHash

from core.config import settings

password_hasher = PasswordHash.recommended()


def verify_password(plain_password: str, stored_hash: str) -> bool:
    return password_hasher.verify(plain_password, stored_hash)


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    expires = datetime.now(UTC) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    payload: dict[str, Any] = {"sub": subject, "exp": expires, "type": "access"}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def decode_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError as exc:
        raise ValueError("Invalid token") from exc
