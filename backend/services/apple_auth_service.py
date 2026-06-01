import json
from datetime import UTC, datetime
from functools import lru_cache
from typing import Any
from urllib.request import urlopen

from fastapi import HTTPException, status
from jose import jwt

from core.config import settings

APPLE_JWKS_URL = "https://appleid.apple.com/auth/keys"
APPLE_ISSUER = "https://appleid.apple.com"


class AppleIdentityVerifier:
    def verify(self, identity_token: str) -> dict[str, Any]:
        if not settings.apple_client_ids:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Sign in with Apple is not configured",
            )

        header = jwt.get_unverified_header(identity_token)
        key = self._key_for_id(header.get("kid"))
        if key is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Apple identity token",
            )

        try:
            claims = jwt.decode(
                identity_token,
                key,
                algorithms=[header.get("alg", "RS256")],
                issuer=APPLE_ISSUER,
                options={"verify_aud": False},
            )
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Apple identity token",
            ) from exc

        if claims.get("aud") not in settings.apple_client_ids:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Apple identity token audience",
            )

        expires_at = datetime.fromtimestamp(int(claims["exp"]), tz=UTC)
        if expires_at <= datetime.now(UTC):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Expired Apple identity token",
            )
        return claims

    def _key_for_id(self, key_id: str | None) -> dict[str, Any] | None:
        if key_id is None:
            return None
        for key in _apple_jwks()["keys"]:
            if key.get("kid") == key_id:
                return key
        return None


@lru_cache(maxsize=1)
def _apple_jwks() -> dict[str, Any]:
    with urlopen(APPLE_JWKS_URL, timeout=10) as response:
        return json.loads(response.read())
