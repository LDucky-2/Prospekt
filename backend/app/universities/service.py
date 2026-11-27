"""Prospectus business rules and conversion between API and database models."""

from datetime import datetime, timezone

from app.universities.models import (
    EligibilityRule,
    FeeStructure,
    ImportantDate,
    MarkDistribution,
    Prospectus,
    SeatInfo,
    Unit,
    University,
)
from app.universities.repository import UniversityRepository
from app.universities.schemas import (
    ProspectusCreate,
    ProspectusUpdate,
    UniversityCreate,
    UniversityUpdate,
    UnitInput,
)


class UniversityService:
    def __init__(self, repository: UniversityRepository) -> None:
        self.repository = repository

    def list_universities(self) -> list[University]:
        return self.repository.list()

    def get_university(self, university_id: int) -> University | None:
        return self.repository.get(university_id)

    def create_university(self, data: UniversityCreate) -> University:
        university = University.model_validate(data)
        return self.repository.create(university)

    def update_university(self, university: University, data: UniversityUpdate) -> University:
        changes = data.model_dump()
        changes["updated_at"] = datetime.now(timezone.utc)
        return self.repository.update(university, changes)

    def create_prospectus(
        self, university: University, data: ProspectusCreate
    ) -> Prospectus:
        if university.id is None:
            raise ValueError("A prospectus requires a saved university.")
        prospectus = Prospectus.model_validate(
            data,
            update={
                "university_id": university.id,
                "units": self._create_units(data.units),
            },
        )
        return self.repository.create_prospectus(prospectus)

    def update_prospectus(
        self, prospectus: Prospectus, data: ProspectusUpdate
    ) -> Prospectus:
        changes = data.model_dump(exclude={"units"})
        changes["updated_at"] = datetime.now(timezone.utc)
        return self.repository.update_prospectus(
            prospectus, changes, self._create_units(data.units)
        )

    def get_prospectus(
        self, university_id: int, prospectus_id: int
    ) -> Prospectus | None:
        return self.repository.get_prospectus(university_id, prospectus_id)

    def delete_prospectus(self, prospectus: Prospectus) -> None:
        self.repository.delete_prospectus(prospectus)

    def delete_university(self, university: University) -> None:
        self.repository.delete(university)

    @staticmethod
    def _create_units(data: list[UnitInput]) -> list[Unit]:
        units = []
        for item in data:
            unit = Unit(
                unit_name=item.unit_name,
                background=item.background,
                total_seats=item.total_seats,
            )
            if item.eligibility_rule is not None:
                unit.eligibility_rule = EligibilityRule.model_validate(item.eligibility_rule)
            if item.mark_distribution is not None:
                unit.mark_distribution = MarkDistribution.model_validate(item.mark_distribution)
            if item.seat_info is not None:
                unit.seat_info = SeatInfo.model_validate(item.seat_info)
            if item.important_date is not None:
                unit.important_date = ImportantDate.model_validate(item.important_date)
            if item.fee_structure is not None:
                unit.fee_structure = FeeStructure.model_validate(item.fee_structure)
            units.append(unit)
        return units
