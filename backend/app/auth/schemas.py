from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from app.auth.models import UserRole


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    expires_in: int
    token_type: str = "bearer"


class UserRead(BaseModel):
    id: UUID
    email: str
    name: str
    role: UserRole
    is_active: bool
    last_login_at: datetime | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8)


class ProfileUpdateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class SessionRead(BaseModel):
    id: UUID
    ip_address: str | None = None
    user_agent: str | None = None
    created_at: datetime
    last_used_at: datetime
