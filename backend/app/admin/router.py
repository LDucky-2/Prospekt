# Admin-only HTTP routes for account management and audit logs.
# contains all the endpoints for the admin panel(user management and activity log viewing).

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request

from app.auth.dependencies import AuthRepositoryDep, CurrentUser
from app.auth.models import AppUser, UserRole
from app.auth.repository import AuthRepository
from app.auth.schemas import (
    EditorCreateRequest,
    UserRead,
    UserRoleUpdateRequest,
    UserStatusUpdateRequest,
)
from app.auth.security import hash_password, utc_now
from app.database import SessionDep
from app.activity.models import ActivityAction
from app.activity.recorder import record_activity
from app.activity.repository import ActivityRepository
from app.activity.schemas import ActivityRead
from app.rbac.dependencies import require_permission
from app.rbac.permissions import Permission

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])

# Admin account actions reject changes to the current administrator's own account.
def ensure_not_self(current_user: AppUser, target_id: UUID) -> None:
    if current_user.id == target_id:
        raise HTTPException(status_code=403, detail="You cannot change your own account from this action")


@router.get(
    "/users",
    response_model=dict,
    dependencies=[Depends(require_permission(Permission.ADMIN_USERS_VIEW))],
)
def list_users(
    search: str | None = None,
    role: str | None = None,
    status: str | None = None,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    repository: AuthRepositoryDep = None,
) -> dict:
    is_active = None
    if status == "active":
        is_active = True
    elif status == "inactive":
        is_active = False

    users, total = repository.list_users(search, role, is_active, offset, limit)
    return {
        "items": [UserRead.model_validate(user, from_attributes=True) for user in users],
        "total": total,
        "offset": offset,
        "limit": limit,
    }


@router.post(
    "/users",
    response_model=UserRead,
    status_code=201,
    dependencies=[Depends(require_permission(Permission.ADMIN_USERS_MANAGE))],
)
def create_editor(
    data: EditorCreateRequest,
    current_user: CurrentUser,
    repository: AuthRepositoryDep,
    request: Request,
    session: SessionDep,
) -> AppUser:
    # Only admins can create editor accounts; all new accounts start as editors.
    existing = repository.get_user_by_email(str(data.email))
    if existing is not None:
        raise HTTPException(status_code=409, detail="An account with this email already exists")

    user = AppUser(
        email=str(data.email).lower(),
        name=data.name.strip(),
        password_hash=hash_password(data.password),
        role=UserRole.EDITOR,
        is_active=True,
    )
    repository.save(user)
    record_activity(
        session,
        ActivityAction.ACCOUNT_CREATED,
        request=request,
        account=current_user,
        target_id=str(user.id),
        detail=f"Created editor {user.email}",
    )
    return user


@router.patch(
    "/users/{user_id}/role",
    response_model=UserRead,
    dependencies=[Depends(require_permission(Permission.ADMIN_USERS_MANAGE))],
)
def change_role(
    user_id: UUID,
    data: UserRoleUpdateRequest,
    current_user: CurrentUser,
    repository: AuthRepositoryDep,
    request: Request,
    session: SessionDep,
) -> AppUser:
    ensure_not_self(current_user, user_id)
    user = repository.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = data.role
    user.updated_at = utc_now()
    repository.save(user)
    action = ActivityAction.ROLE_PROMOTED if data.role == UserRole.ADMIN else ActivityAction.ROLE_DEMOTED
    record_activity(
        session,
        action,
        request=request,
        account=current_user,
        target_id=str(user.id),
        detail=f"Changed {user.email} role to {data.role.value}",
    )
    return user


@router.patch(
    "/users/{user_id}/status",
    response_model=UserRead,
    dependencies=[Depends(require_permission(Permission.ADMIN_USERS_MANAGE))],
)
def change_status(
    user_id: UUID,
    data: UserStatusUpdateRequest,
    current_user: CurrentUser,
    repository: AuthRepositoryDep,
    request: Request,
    session: SessionDep,
) -> AppUser:
    ensure_not_self(current_user, user_id)
    user = repository.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = data.is_active
    user.updated_at = utc_now()
    if not data.is_active:
        now = utc_now()
        repository.revoke_all_sessions(user.id, now)
    repository.save(user)
    action = ActivityAction.ACCOUNT_ACTIVATED if data.is_active else ActivityAction.ACCOUNT_DEACTIVATED
    record_activity(
        session,
        action,
        request=request,
        account=current_user,
        target_id=str(user.id),
        detail=f"{'Activated' if data.is_active else 'Deactivated'} {user.email}",
    )
    return user


@router.delete(
    "/users/{user_id}",
    status_code=204,
    dependencies=[Depends(require_permission(Permission.ADMIN_USERS_MANAGE))],
)
def delete_user(
    user_id: UUID,
    current_user: CurrentUser,
    repository: AuthRepositoryDep,
    request: Request,
    session: SessionDep,
) -> None:
    ensure_not_self(current_user, user_id)
    user = repository.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    repository.revoke_all_sessions(user.id, utc_now())
    ActivityRepository(session).detach_account_history(user.id, user.email)
    repository.delete_user(user)
    record_activity(
        session,
        ActivityAction.ACCOUNT_DELETED,
        request=request,
        account=current_user,
        target_id=str(user_id),
        detail=f"Deleted account {user.email}",
    )


@router.get(
    "/logs",
    response_model=dict,
    dependencies=[Depends(require_permission(Permission.ADMIN_LOGS_VIEW))],
)
def list_logs(
    search: str | None = None,
    action: str | None = None,
    ip_address: str | None = None,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    session: SessionDep = None,
) -> dict:
    """List filtered audit and security events for the admin Logs page."""
    activity_repository = ActivityRepository(session)
    entries, total = activity_repository.list(search, action, ip_address, offset, limit)
    return {
        "items": [ActivityRead.model_validate(entry, from_attributes=True) for entry in entries],
        "total": total,
        "offset": offset,
        "limit": limit,
    }
