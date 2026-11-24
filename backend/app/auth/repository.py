"""Database operations for users and refresh-token sessions."""

from datetime import datetime
from uuid import UUID

from sqlmodel import Session, select

from app.auth.models import AppUser, RefreshToken


class AuthRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_user_by_email(self, email: str) -> AppUser | None:
        return self.session.exec(select(AppUser).where(AppUser.email == email.lower())).first()

    def get_user_by_id(self, user_id: UUID) -> AppUser | None:
        return self.session.exec(select(AppUser).where(AppUser.id == user_id)).first()

    def get_refresh_token(self, token_hash: str) -> RefreshToken | None:
        return self.session.exec(select(RefreshToken).where(RefreshToken.token_hash == token_hash)).first()

    def save(self, record: AppUser | RefreshToken) -> None:
        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)

    def delete_user(self, user: AppUser) -> None:
        self.session.delete(user)
        self.session.commit()

    def list_users(self, search: str | None = None, role: str | None = None,
                   is_active: bool | None = None, offset: int = 0, limit: int = 20) -> tuple[list[AppUser], int]:
        """List admin/editor accounts with optional search, role and status filters."""
        statement = select(AppUser)
        count_statement = select(AppUser)

        if search:
            pattern = f"%{search.lower()}%"
            statement = statement.where(
                (AppUser.name.ilike(pattern)) | (AppUser.email.ilike(pattern))
            )
            count_statement = count_statement.where(
                (AppUser.name.ilike(pattern)) | (AppUser.email.ilike(pattern))
            )
        if role:
            statement = statement.where(AppUser.role == role)
            count_statement = count_statement.where(AppUser.role == role)
        if is_active is not None:
            statement = statement.where(AppUser.is_active == is_active)
            count_statement = count_statement.where(AppUser.is_active == is_active)

        total = len(list(self.session.exec(count_statement).all()))
        statement = statement.order_by(AppUser.created_at.desc()).offset(offset).limit(limit)
        return list(self.session.exec(statement).all()), total

    def revoke_refresh_token(self, record: RefreshToken, now: datetime) -> None:
        record.revoked_at = now
        self.save(record)

    def list_sessions(self, user_id: UUID) -> list[RefreshToken]:
        statement = (
            select(RefreshToken)
            .where(RefreshToken.user_id == user_id, RefreshToken.revoked_at.is_(None))
            .order_by(RefreshToken.last_used_at.desc())
        )
        return list(self.session.exec(statement).all())

    def revoke_session(self, user_id: UUID, session_id: UUID, now: datetime) -> bool:
        statement = select(RefreshToken).where(
            RefreshToken.user_id == user_id,
            RefreshToken.session_id == session_id,
            RefreshToken.revoked_at.is_(None),
        )
        record = self.session.exec(statement).first()
        if record is None:
            return False
        record.revoked_at = now
        self.save(record)
        return True

    def revoke_all_sessions(self, user_id: UUID, now: datetime) -> int:
        statement = select(RefreshToken).where(
            RefreshToken.user_id == user_id,
            RefreshToken.revoked_at.is_(None),
        )
        records = list(self.session.exec(statement).all())
        for record in records:
            record.revoked_at = now
        for record in records:
            self.session.add(record)
        self.session.commit()
        return len(records)
