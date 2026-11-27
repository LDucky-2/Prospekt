# API response schemas for audit log entries.

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.activity.models import ActivityAction


class ActivityRead(BaseModel):
    id: UUID
    action: ActivityAction
    account_id: UUID | None = None
    account_email: str | None = None
    target_id: str | None = None
    detail: str | None = None
    ip_address: str | None = None
    user_agent: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
