"""Database queries for searchable and paginated activity logs."""

from sqlmodel import Session, select

from app.activity.models import ActivityAction, ActivityLog


class ActivityRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list(
        self,
        search: str | None = None,
        action: str | None = None,
        ip_address: str | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[ActivityLog], int]:
        statement = select(ActivityLog)
        count_statement = select(ActivityLog)

        if action:
            try:
                action_value = ActivityAction(action)
                statement = statement.where(ActivityLog.action == action_value)
                count_statement = count_statement.where(ActivityLog.action == action_value)
            except ValueError:
                action_value = None

        if ip_address:
            statement = statement.where(ActivityLog.ip_address == ip_address)
            count_statement = count_statement.where(ActivityLog.ip_address == ip_address)

        if search:
            pattern = f"%{search.lower()}%"
            statement = statement.where(
                (ActivityLog.account_email.ilike(pattern))
                | (ActivityLog.detail.ilike(pattern))
                | (ActivityLog.target_id.ilike(pattern))
            )
            count_statement = count_statement.where(
                (ActivityLog.account_email.ilike(pattern))
                | (ActivityLog.detail.ilike(pattern))
                | (ActivityLog.target_id.ilike(pattern))
            )

        total = len(list(self.session.exec(count_statement).all()))
        statement = statement.order_by(ActivityLog.created_at.desc()).offset(offset).limit(limit)
        return list(self.session.exec(statement).all()), total
