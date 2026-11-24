"""Permission constants shared by backend authorization checks."""

from enum import Enum


class Permission(str, Enum):
    UNIVERSITY_CREATE = "university:create"
    PROSPECTUS_CREATE = "prospectus:create"
    PROSPECTUS_UPDATE = "prospectus:update"
    PROSPECTUS_DELETE = "prospectus:delete"
    ADMIN_USERS_VIEW = "admin:users:view"
    ADMIN_USERS_MANAGE = "admin:users:manage"
    ADMIN_LOGS_VIEW = "admin:logs:view"
