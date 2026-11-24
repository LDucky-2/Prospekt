"""Database model and action names for audit and security activity logs."""

from datetime import datetime, timezone
from enum import Enum
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class ActivityAction(str, Enum):
    LOGIN_SUCCESS = "login_success"
    LOGIN_FAILED = "login_failed"
    LOGOUT = "logout"
    PASSWORD_CHANGE = "password_change"
    ACCOUNT_CREATED = "account_created"
    ACCOUNT_DELETED = "account_deleted"
    ACCOUNT_ACTIVATED = "account_activated"
    ACCOUNT_DEACTIVATED = "account_deactivated"
    ROLE_PROMOTED = "role_promoted"
    ROLE_DEMOTED = "role_demoted"
    UNIVERSITY_CREATED = "university_created"
    UNIVERSITY_UPDATED = "university_updated"
    UNIVERSITY_DELETED = "university_deleted"
    ACCESS_DENIED = "access_denied"


class ActivityLog(SQLModel, table=True):
    __tablename__ = "activity_log"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    action: ActivityAction = Field(index=True)
    account_id: UUID | None = Field(default=None, foreign_key="app_user.id", index=True)
    account_email: str | None = Field(default=None, max_length=254)
    target_id: str | None = Field(default=None, max_length=100)
    detail: str | None = Field(default=None, max_length=1000)
    ip_address: str | None = Field(default=None, max_length=45, index=True)
    user_agent: str | None = Field(default=None, max_length=300)
    created_at: datetime = Field(default_factory=utc_now, index=True)
