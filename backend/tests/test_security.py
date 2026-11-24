from datetime import timedelta
from uuid import uuid4

import jwt
import pytest
from fastapi import HTTPException

from app.auth.models import AppUser, UserRole
from app.auth.security import create_access_token, utc_now
from app.config import settings
from app.rbac.dependencies import require_permission
from app.rbac.permissions import Permission
from app.universities.schemas import EligibilityRuleInput, MarkDistributionInput


def test_missing_or_tampered_access_token_is_rejected() -> None:
    token = create_access_token(uuid4(), "editor")
    with pytest.raises(jwt.PyJWTError):
        jwt.decode(f"{token}-tampered", settings.JWT_SECRET, algorithms=["HS256"])


def test_expired_access_token_is_rejected() -> None:
    now = utc_now()
    token = jwt.encode(
        {"sub": str(uuid4()), "role": "editor", "iat": now - timedelta(minutes=20), "exp": now - timedelta(minutes=5)},
        settings.JWT_SECRET,
        algorithm="HS256",
    )
    with pytest.raises(jwt.ExpiredSignatureError):
        jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])


def test_editor_cannot_create_universities() -> None:
    editor = AppUser(
        email="editor@example.com",
        name="Test Editor",
        password_hash="unused",
        role=UserRole.EDITOR,
    )
    check = require_permission(Permission.UNIVERSITY_CREATE)
    with pytest.raises(HTTPException) as exc:
        check(editor)
    assert exc.value.status_code == 403


def test_admin_can_create_universities() -> None:
    admin = AppUser(
        email="admin@example.com",
        name="Test Admin",
        password_hash="unused",
        role=UserRole.ADMIN,
    )
    check = require_permission(Permission.UNIVERSITY_CREATE)
    assert check(admin).role == UserRole.ADMIN


def test_editor_has_prospectus_permissions_but_not_account_permissions() -> None:
    editor = AppUser(
        email="editor@example.com",
        name="Test Editor",
        password_hash="unused",
        role=UserRole.EDITOR,
    )

    assert require_permission(Permission.PROSPECTUS_UPDATE)(editor).role == UserRole.EDITOR
    with pytest.raises(HTTPException) as exc:
        require_permission(Permission.ADMIN_USERS_MANAGE)(editor)
    assert exc.value.status_code == 403


def test_string_fields_accept_non_numeric_text() -> None:
    eligibility = EligibilityRuleInput(
        min_ssc_gpa="about four",
        combined_gpa="not specified",
    )
    marks = MarkDistributionInput(
        total_marks="hundreds",
        mcq_marks="varies",
    )
    assert eligibility.min_ssc_gpa == "about four"
    assert eligibility.combined_gpa == "not specified"
    assert marks.total_marks == "hundreds"
    assert marks.mcq_marks == "varies"
