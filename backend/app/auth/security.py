import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
from pwdlib import PasswordHash

from app.config import settings

password_hash = PasswordHash.recommended()

# Password and token helpers keep cryptographic details out of routers and services.

def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def hash_password(password: str) -> str:
    """Hash with Argon2 plus the deployment-only server pepper."""
    return password_hash.hash(f"{settings.PASSWORD_PEPPER}{password}")


def verify_password(password: str, hashed: str) -> bool:
    return password_hash.verify(f"{settings.PASSWORD_PEPPER}{password}", hashed)


def create_access_token(user_id: UUID, role: str) -> str:
    # Access tokens are short-lived and identify the account and role.
    now = utc_now()
    return jwt.encode(
        {
            "sub": str(user_id),
            "role": role,
            "iat": now,
            "exp": now + timedelta(minutes=settings.ACCESS_TOKEN_MINUTES),
        },
        settings.JWT_SECRET,
        algorithm="HS256",
    )


def create_refresh_token() -> str:
    return secrets.token_urlsafe(48)


def hash_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
