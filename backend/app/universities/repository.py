"""Database queries for listing, loading, creating and deleting universities."""

from __future__ import annotations

from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from app.universities.models import Prospectus, Unit, University


class UniversityRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list(self) -> list[University]:
        statement = (
            select(University)
            .options(
                *self._prospectus_load_options(),
            )
            .order_by(University.name, University.id)
        )
        return list(self.session.exec(statement).all())

    def get(self, university_id: int) -> University | None:
        statement = (
            select(University)
            .where(University.id == university_id)
            .options(
                *self._prospectus_load_options(),
            )
        )
        return self.session.exec(statement).first()

    def get_prospectus(
        self, university_id: int, prospectus_id: int
    ) -> Prospectus | None:
        statement = (
            select(Prospectus)
            .where(
                Prospectus.id == prospectus_id,
                Prospectus.university_id == university_id,
            )
            .options(*self._unit_load_options())
        )
        return self.session.exec(statement).first()

    def create(self, university: University) -> University:
        return self._save(university)

    def update(self, university: University, changes: dict) -> University:
        university.sqlmodel_update(changes)
        return self._save(university)

    def create_prospectus(self, prospectus: Prospectus) -> Prospectus:
        return self._save_prospectus(prospectus)

    def update_prospectus(
        self, prospectus: Prospectus, changes: dict, units: list[Unit]
    ) -> Prospectus:
        prospectus.sqlmodel_update(changes)
        prospectus.units = units
        return self._save_prospectus(prospectus)

    def delete_prospectus(self, prospectus: Prospectus) -> None:
        self.session.delete(prospectus)
        self.session.commit()

    def delete(self, university: University) -> None:
        self.session.delete(university)
        self.session.commit()

    def _save(self, university: University) -> University:
        self.session.add(university)
        self.session.commit()
        self.session.refresh(university)
        return university

    def _save_prospectus(self, prospectus: Prospectus) -> Prospectus:
        self.session.add(prospectus)
        self.session.commit()
        self.session.refresh(prospectus)
        return prospectus

    @staticmethod
    def _prospectus_load_options():
        return (
            selectinload(University.prospectuses).selectinload(Prospectus.units).selectinload(Unit.eligibility_rule),
            selectinload(University.prospectuses).selectinload(Prospectus.units).selectinload(Unit.mark_distribution),
            selectinload(University.prospectuses).selectinload(Prospectus.units).selectinload(Unit.seat_info),
            selectinload(University.prospectuses).selectinload(Prospectus.units).selectinload(Unit.important_date),
            selectinload(University.prospectuses).selectinload(Prospectus.units).selectinload(Unit.fee_structure),
        )

    @staticmethod
    def _unit_load_options():
        return (
            selectinload(Prospectus.units).selectinload(Unit.eligibility_rule),
            selectinload(Prospectus.units).selectinload(Unit.mark_distribution),
            selectinload(Prospectus.units).selectinload(Unit.seat_info),
            selectinload(Prospectus.units).selectinload(Unit.important_date),
            selectinload(Prospectus.units).selectinload(Unit.fee_structure),
        )
