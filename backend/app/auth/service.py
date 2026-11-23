from datetime import timedelta
from uuid import UUID, uuid4

from fastapi import HTTPException, Request

from app.auth.models import AppUser, RefreshToken
from app.auth.repository import AuthRepository
from app.auth.schemas import LoginRequest, PasswordChangeRequest, ProfileUpdateRequest
from app.auth.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    hash_refresh_token,
    utc_now,
    verify_password,
)
from app.config import settings


class AuthService:
    def __init__(self, repository: AuthRepository) -> None:
        self.repository = repository

    def login(self, data: LoginRequest, request: Request) -> tuple[AppUser, str, str]:
        """Authenticate, enforce lockout, and create a rotated refresh session."""
        user = self.repository.get_user_by_email(data.email)
        now = utc_now()

        if user is None:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        if not user.is_active:
            raise HTTPException(status_code=403, detail="Account is inactive")
        if user.locked_until is not None and user.locked_until > now:
            raise HTTPException(status_code=423, detail="Account is temporarily locked")

        if not verify_password(data.password, user.password_hash):
            user.failed_login_count += 1
            if user.failed_login_count >= 5:
                user.locked_until = now + timedelta(minutes=15)
            user.updated_at = now
            self.repository.save(user)
            raise HTTPException(status_code=401, detail="Invalid email or password")

        user.failed_login_count = 0
        user.locked_until = None
        user.last_login_at = now
        user.updated_at = now
        self.repository.save(user)

        access_token = create_access_token(user.id, user.role.value)
        refresh_token = create_refresh_token()
        session_id = uuid4()
        ip_address = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")

        refresh_record = RefreshToken(
            user_id=user.id,
            session_id=session_id,
            token_hash=hash_refresh_token(refresh_token),
            expires_at=now + timedelta(days=settings.REFRESH_TOKEN_DAYS),
            ip_address=ip_address,
            user_agent=user_agent[:300] if user_agent else None,
            created_at=now,
            last_used_at=now,
        )
        self.repository.save(refresh_record)
        return user, access_token, refresh_token

    def refresh(self, raw_token: str | None, request: Request) -> tuple[str, str]:
        if not raw_token:
            raise HTTPException(status_code=401, detail="Refresh session missing")

        now = utc_now()
        record = self.repository.get_refresh_token(hash_refresh_token(raw_token))
        if record is None:
            raise HTTPException(status_code=401, detail="Invalid refresh session")
        if record.revoked_at is not None:
            self.repository.revoke_all_sessions(record.user_id, now)
            raise HTTPException(status_code=401, detail="Refresh session reuse detected")
        if record.expires_at < now:
            record.revoked_at = now
            self.repository.save(record)
            raise HTTPException(status_code=401, detail="Refresh session expired")

        user = self.repository.get_user_by_id(record.user_id)
        if user is None or not user.is_active:
            raise HTTPException(status_code=401, detail="Invalid refresh session")

        record.revoked_at = now
        self.repository.save(record)

        refresh_token = create_refresh_token()
        ip_address = request.client.host if request.client else record.ip_address
        user_agent = request.headers.get("user-agent")
        new_record = RefreshToken(
            user_id=user.id,
            session_id=record.session_id,
            token_hash=hash_refresh_token(refresh_token),
            expires_at=now + timedelta(days=settings.REFRESH_TOKEN_DAYS),
            ip_address=ip_address,
            user_agent=user_agent[:300] if user_agent else record.user_agent,
            created_at=record.created_at,
            last_used_at=now,
        )
        self.repository.save(new_record)
        return create_access_token(user.id, user.role.value), refresh_token

    def logout(self, raw_token: str | None) -> None:
        if not raw_token:
            return
        record = self.repository.get_refresh_token(hash_refresh_token(raw_token))
        if record is not None:
            self.repository.revoke_refresh_token(record, utc_now())

    def list_sessions(self, user: AppUser) -> list[RefreshToken]:
        return self.repository.list_sessions(user.id)

    def revoke_session(self, user: AppUser, session_id: UUID) -> bool:
        return self.repository.revoke_session(user.id, session_id, utc_now())

    def revoke_all_sessions(self, user: AppUser) -> int:
        return self.repository.revoke_all_sessions(user.id, utc_now())

    def update_profile(self, user: AppUser, data: ProfileUpdateRequest) -> AppUser:
        user.name = data.name
        user.updated_at = utc_now()
        self.repository.save(user)
        return user

    def change_password(self, user: AppUser, data: PasswordChangeRequest) -> None:
        if not verify_password(data.current_password, user.password_hash):
            raise HTTPException(status_code=400, detail="Current password is incorrect")
        user.password_hash = hash_password(data.new_password)
        user.updated_at = utc_now()
        self.repository.save(user)
