from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from app.universities.models import Unit, University


class UniversityRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list(self) -> list[University]:
        statement = (
            select(University)
            .options(
                selectinload(University.units).selectinload(Unit.eligibility_rule),
                selectinload(University.units).selectinload(Unit.mark_distribution),
                selectinload(University.units).selectinload(Unit.seat_info),
                selectinload(University.units).selectinload(Unit.important_date),
                selectinload(University.units).selectinload(Unit.fee_structure),
            )
            .order_by(University.name, University.id)
        )
        return list(self.session.exec(statement).all())

    def get(self, university_id: int) -> University | None:
        statement = (
            select(University)
            .where(University.id == university_id)
            .options(
                selectinload(University.units).selectinload(Unit.eligibility_rule),
                selectinload(University.units).selectinload(Unit.mark_distribution),
                selectinload(University.units).selectinload(Unit.seat_info),
                selectinload(University.units).selectinload(Unit.important_date),
                selectinload(University.units).selectinload(Unit.fee_structure),
            )
        )
        return self.session.exec(statement).first()

    def create(self, university: University) -> University:
        return self._save(university)

    def update(self, university: University, changes: dict, units: list[Unit]) -> University:
        university.sqlmodel_update(changes)
        university.units = units
        return self._save(university)

    def delete(self, university: University) -> None:
        self.session.delete(university)
        self.session.commit()

    def _save(self, university: University) -> University:
        self.session.add(university)
        self.session.commit()
        self.session.refresh(university)
        return university
