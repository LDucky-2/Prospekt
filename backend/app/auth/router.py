from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, Response

from app.auth.dependencies import AuthRepositoryDep, CurrentUser
from app.auth.models import AppUser
from app.auth.repository import AuthRepository
from app.auth.schemas import (
    LoginRequest,
    PasswordChangeRequest,
    ProfileUpdateRequest,
    SessionRead,
    TokenResponse,
    UserRead,
)
from app.auth.service import AuthService
from app.config import settings
from app.database import SessionDep

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])
COOKIE_NAME = "prospekt_refresh"


def get_auth_service(session: SessionDep) -> AuthService:
    return AuthService(AuthRepository(session))


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


def set_refresh_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        COOKIE_NAME,
        token,
        max_age=settings.REFRESH_TOKEN_DAYS * 24 * 60 * 60,
        httponly=True,
        secure=bool(settings.VERCEL),
        samesite="strict",
        path="/api/v1/auth",
    )


def clear_refresh_cookie(response: Response) -> None:
    response.delete_cookie(COOKIE_NAME, path="/api/v1/auth", httponly=True, samesite="strict")


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, request: Request, response: Response, service: AuthServiceDep) -> TokenResponse:
    user, access_token, refresh_token = service.login(data, request)
    set_refresh_cookie(response, refresh_token)
    return TokenResponse(access_token=access_token, expires_in=settings.ACCESS_TOKEN_MINUTES * 60)


@router.post("/refresh", response_model=TokenResponse)
def refresh(
    request: Request,
    response: Response,
    service: AuthServiceDep,
    refresh_token: Annotated[str | None, Cookie(alias=COOKIE_NAME)] = None,
) -> TokenResponse:
    access_token, new_refresh_token = service.refresh(refresh_token, request)
    set_refresh_cookie(response, new_refresh_token)
    return TokenResponse(access_token=access_token, expires_in=settings.ACCESS_TOKEN_MINUTES * 60)


@router.post("/logout", status_code=204)
def logout(
    response: Response,
    service: AuthServiceDep,
    refresh_token: Annotated[str | None, Cookie(alias=COOKIE_NAME)] = None,
) -> None:
    service.logout(refresh_token)
    clear_refresh_cookie(response)


@router.get("/me", response_model=UserRead)
def get_me(user: CurrentUser) -> AppUser:
    return user


@router.patch("/me", response_model=UserRead)
def update_profile(data: ProfileUpdateRequest, user: CurrentUser, service: AuthServiceDep) -> AppUser:
    return service.update_profile(user, data)


@router.post("/password", status_code=204)
def change_password(data: PasswordChangeRequest, user: CurrentUser, service: AuthServiceDep) -> None:
    service.change_password(user, data)


@router.get("/sessions", response_model=list[SessionRead])
def list_sessions(user: CurrentUser, service: AuthServiceDep) -> list[SessionRead]:
    return [SessionRead.model_validate(session, from_attributes=True) for session in service.list_sessions(user)]


@router.delete("/sessions/{session_id}", status_code=204)
def revoke_session(session_id: UUID, user: CurrentUser, service: AuthServiceDep) -> None:
    if not service.revoke_session(user, session_id):
        raise HTTPException(status_code=404, detail="Session not found")
