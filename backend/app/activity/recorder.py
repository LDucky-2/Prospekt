from fastapi import Request
from sqlmodel import Session

from app.activity.models import ActivityAction, ActivityLog
from app.auth.models import AppUser


def request_info(request: Request | None) -> tuple[str | None, str | None]:
    if request is None:
        return None, None
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    return ip_address, user_agent[:300] if user_agent else None


def record_activity(
    session: Session,
    action: ActivityAction,
    request: Request | None = None,
    account: AppUser | None = None,
    account_email: str | None = None,
    target_id: str | None = None,
    detail: str | None = None,
) -> ActivityLog:
    """Write one audit event and include client information when available."""
    ip_address, user_agent = request_info(request)
    entry = ActivityLog(
        action=action,
        account_id=account.id if account else None,
        account_email=account.email if account else account_email,
        target_id=target_id,
        detail=detail,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry
