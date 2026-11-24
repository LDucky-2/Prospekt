"""Reusable FastAPI permission checks for role-based authorization."""

from collections.abc import Callable
from typing import Annotated

from fastapi import Depends, HTTPException

from app.auth.dependencies import CurrentUser
from app.auth.models import AppUser, UserRole
from app.rbac.permissions import Permission

ROLE_PERMISSIONS: dict[UserRole, set[Permission]] = {
    UserRole.EDITOR: {
        Permission.PROSPECTUS_CREATE,
        Permission.PROSPECTUS_UPDATE,
        Permission.PROSPECTUS_DELETE,
    },
    UserRole.ADMIN: {
        Permission.UNIVERSITY_CREATE,
        Permission.PROSPECTUS_CREATE,
        Permission.PROSPECTUS_UPDATE,
        Permission.PROSPECTUS_DELETE,
        Permission.ADMIN_USERS_VIEW,
        Permission.ADMIN_USERS_MANAGE,
        Permission.ADMIN_LOGS_VIEW,
    },
}


def require_permission(permission: Permission) -> Callable[..., AppUser]:
    """Reusable server-side permission dependency used by all protected routes."""

    def check(user: CurrentUser) -> AppUser:
        if permission not in ROLE_PERMISSIONS.get(user.role, set()):
            raise HTTPException(status_code=403, detail="Permission denied")
        return user

    return check
