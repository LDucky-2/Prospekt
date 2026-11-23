from datetime import datetime, timezone
from enum import Enum
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class UserRole(str, Enum):
    EDITOR = "editor"
    ADMIN = "admin"


class AppUser(SQLModel, table=True):
    __tablename__ = "app_user"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(max_length=254, unique=True, index=True)
    name: str = Field(max_length=100)
    password_hash: str
    role: UserRole = Field(default=UserRole.EDITOR)
    is_active: bool = Field(default=True)
    failed_login_count: int = Field(default=0)
    locked_until: datetime | None = None
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    last_login_at: datetime | None = None


class RefreshToken(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="app_user.id", index=True, ondelete="CASCADE")
    session_id: UUID = Field(index=True)
    token_hash: str = Field(max_length=64, unique=True)
    expires_at: datetime
    revoked_at: datetime | None = None
    created_at: datetime = Field(default_factory=utc_now)
    last_used_at: datetime = Field(default_factory=utc_now)
    ip_address: str | None = Field(default=None, max_length=45)
    user_agent: str | None = Field(default=None, max_length=300)
