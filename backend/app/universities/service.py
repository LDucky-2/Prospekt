from datetime import datetime, timezone

from app.universities.models import (
    EligibilityRule,
    FeeStructure,
    ImportantDate,
    MarkDistribution,
    SeatInfo,
    Unit,
    University,
)
from app.universities.repository import UniversityRepository
from app.universities.schemas import UniversityCreate, UniversityUpdate, UnitInput


class UniversityService:
    def __init__(self, repository: UniversityRepository) -> None:
        self.repository = repository

    def list_universities(self) -> list[University]:
        return self.repository.list()

    def get_university(self, university_id: int) -> University | None:
        return self.repository.get(university_id)

    def create_university(self, data: UniversityCreate) -> University:
        university = University.model_validate(data, update={"units": self._create_units(data.units)})
        return self.repository.create(university)

    def update_university(self, university: University, data: UniversityUpdate) -> University:
        changes = data.model_dump(exclude={"units"})
        changes["updated_at"] = datetime.now(timezone.utc)
        return self.repository.update(university, changes, self._create_units(data.units))

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
