from datetime import date, datetime, timezone
from typing import Annotated

from pydantic import StringConstraints, field_validator
from pydantic import ConfigDict
from sqlmodel import Field, SQLModel

UniversityName = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=150)]
UniversitySession = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=20)]


class UniversityInput(SQLModel):
    name: UniversityName
    session: UniversitySession
    website_url: str | None = Field(default=None, max_length=500)
    overview: str = Field(max_length=2000)
    application_start: date | None = None
    application_end: date | None = None
    admit_card_download: date | None = None
    exam_date: date | None = None
    units: list["UnitInput"] = Field(default_factory=list)


class EligibilityRuleInput(SQLModel):
    min_ssc_gpa: float | None = None
    min_hsc_gpa: float | None = None
    combined_gpa: float | None = None
    second_time_allowed: bool | None = None
    second_time_penalty_marks: float | None = None
    subject_requirements: str | None = None


class MarkDistributionInput(SQLModel):
    total_marks: int | None = None
    mcq_marks: int | None = None
    written_marks: int | None = None
    negative_marking_penalty: float | None = None
    pass_mark_total: float | None = None
    subject_breakout: str | None = None


class SeatInfoInput(SQLModel):
    general_seats: int | None = None
    quota_breakdown: str | None = None


class ImportantDateInput(SQLModel):
    application_start: date | None = None
    application_end: date | None = None
    admit_card_start: date | None = None
    exam_date: date | None = None


class FeeStructureInput(SQLModel):
    application_fee: float | None = None
    payment_methods: str | None = None


class UnitInput(SQLModel):
    unit_name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=120)]
    background: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=40)]
    total_seats: int | None = None
    eligibility_rule: EligibilityRuleInput | None = None
    mark_distribution: MarkDistributionInput | None = None
    seat_info: SeatInfoInput | None = None
    important_date: ImportantDateInput | None = None
    fee_structure: FeeStructureInput | None = None


class UniversityCreate(UniversityInput):
    pass


class UniversityUpdate(UniversityInput):
    pass


class UnitRead(UnitInput):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UniversityRead(UniversityInput):
    units: list[UnitRead] = Field(default_factory=list)
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

    @field_validator("created_at", "updated_at")
    @classmethod
    def as_utc(cls, value: datetime) -> datetime:
        return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value


UniversityInput.model_rebuild()
UniversityRead.model_rebuild()
