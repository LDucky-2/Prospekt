from sqlalchemy import event
from sqlmodel import Session, SQLModel, create_engine, select
from starlette.requests import Request

from app.activity.models import ActivityAction, ActivityLog
from app.admin.router import delete_user
from app.auth.models import AppUser, UserRole
from app.auth.repository import AuthRepository


def test_delete_user_preserves_audit_history_with_foreign_keys_enabled() -> None:
    engine = create_engine("sqlite://")

    @event.listens_for(engine, "connect")
    def enable_foreign_keys(connection, _record) -> None:
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        admin = AppUser(
            email="admin@example.com",
            name="Admin",
            password_hash="unused",
            role=UserRole.ADMIN,
        )
        target = AppUser(
            email="editor@example.com",
            name="Editor",
            password_hash="unused",
            role=UserRole.EDITOR,
        )
        session.add_all([admin, target])
        session.commit()
        session.refresh(admin)
        session.refresh(target)

        old_activity = ActivityLog(
            action=ActivityAction.LOGIN_SUCCESS,
            account_id=target.id,
            account_email=target.email,
        )
        session.add(old_activity)
        session.commit()
        target_id = target.id

        request = Request({"type": "http", "headers": [], "client": ("127.0.0.1", 1)})
        delete_user(target_id, admin, AuthRepository(session), request, session)

        assert AuthRepository(session).get_user_by_id(target_id) is None
        preserved_activity = session.get(ActivityLog, old_activity.id)
        assert preserved_activity is not None
        assert preserved_activity.account_id is None
        assert preserved_activity.account_email == "editor@example.com"

        deletion_activity = session.exec(
            select(ActivityLog).where(ActivityLog.action == ActivityAction.ACCOUNT_DELETED)
        ).one()
        assert deletion_activity.account_id == admin.id
        assert deletion_activity.target_id == str(target_id)
