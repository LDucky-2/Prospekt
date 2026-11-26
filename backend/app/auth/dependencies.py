# FastAPI dependencies for authentication and current-user lookup.

from typing import Annotated

import jwt
from fastapi import Depends, Header, HTTPException

from app.auth.models import AppUser
from app.auth.repository import AuthRepository
from app.auth.schemas import LoginRequest
from app.auth.security import utc_now
from app.config import settings
from app.database import SessionDep


def get_auth_repository(session: SessionDep) -> AuthRepository:
    return AuthRepository(session)


AuthRepositoryDep = Annotated[AuthRepository, Depends(get_auth_repository)]


def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
    repository: AuthRepository = Depends(get_auth_repository),
) -> AppUser:
    """Verify JWT signature and current account status for every protected request."""
    # The authorization header must contain a bearer token for protected routes.
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.split(" ", 1)[1].strip()
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        user_id = payload["sub"]
    except (jwt.PyJWTError, KeyError):
        raise HTTPException(status_code=401, detail="Invalid or expired access token")

    from uuid import UUID

    try:
        user = repository.get_user_by_id(UUID(user_id))
    except (ValueError, TypeError):
        raise HTTPException(status_code=401, detail="Invalid or expired access token")
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid or expired access token")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is inactive")
    if user.locked_until is not None and user.locked_until > utc_now():
        raise HTTPException(status_code=423, detail="Account is temporarily locked")
    if payload.get("role") != user.role.value:
        raise HTTPException(status_code=401, detail="Invalid or expired access token")
    return user


CurrentUser = Annotated[AppUser, Depends(get_current_user)]
