"""SQLModel tables for universities, prospectuses, units and admissions data."""

from datetime import date, datetime, timezone

from sqlmodel import Field, Relationship, SQLModel


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class University(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=150, index=True)
    website_url: str | None = Field(default=None, max_length=500)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    prospectuses: list["Prospectus"] = Relationship(back_populates="university", cascade_delete=True)


class Prospectus(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    university_id: int = Field(
        foreign_key="university.id",
        ondelete="CASCADE",
        index=True,
    )
    session: str = Field(max_length=20)
    overview: str = Field(max_length=2000)
    application_start: date | None = None
    application_end: date | None = None
    admit_card_download: date | None = None
    exam_date: date | None = None
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    university: University = Relationship(back_populates="prospectuses")
    units: list["Unit"] = Relationship(back_populates="prospectus", cascade_delete=True)


class Unit(SQLModel, table=True):
    # A prospectus can contain several units, each with separate admissions information.
    id: int | None = Field(default=None, primary_key=True)
    prospectus_id: int | None = Field(
        default=None,
        foreign_key="prospectus.id",
        ondelete="CASCADE",
        index=True,
        nullable=False,
    )
    unit_name: str = Field(max_length=120)
    background: str = Field(max_length=40)
    total_seats: str | None = None
    prospectus: Prospectus = Relationship(back_populates="units")
    eligibility_rule: "EligibilityRule" = Relationship(
        back_populates="unit",
        cascade_delete=True,
        sa_relationship_kwargs={"uselist": False},
    )
    mark_distribution: "MarkDistribution" = Relationship(
        back_populates="unit",
        cascade_delete=True,
        sa_relationship_kwargs={"uselist": False},
    )
    seat_info: "SeatInfo" = Relationship(
        back_populates="unit",
        cascade_delete=True,
        sa_relationship_kwargs={"uselist": False},
    )
    important_date: "ImportantDate" = Relationship(
        back_populates="unit",
        cascade_delete=True,
        sa_relationship_kwargs={"uselist": False},
    )
    fee_structure: "FeeStructure" = Relationship(
        back_populates="unit",
        cascade_delete=True,
        sa_relationship_kwargs={"uselist": False},
    )


class EligibilityRule(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    unit_id: int | None = Field(
        default=None, foreign_key="unit.id", ondelete="CASCADE", unique=True, nullable=False
    )
    min_ssc_gpa: str | None = None
    min_hsc_gpa: str | None = None
    combined_gpa: str | None = None
    second_time_allowed: bool | None = None
    second_time_penalty_marks: str | None = None
    subject_requirements: str | None = None
    unit: Unit = Relationship(back_populates="eligibility_rule")


class MarkDistribution(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    unit_id: int | None = Field(
        default=None, foreign_key="unit.id", ondelete="CASCADE", unique=True, nullable=False
    )
    total_marks: str | None = None
    mcq_marks: str | None = None
    written_marks: str | None = None
    negative_marking_penalty: str | None = None
    pass_mark_total: str | None = None
    subject_breakout: str | None = None
    unit: Unit = Relationship(back_populates="mark_distribution")


class SeatInfo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    unit_id: int | None = Field(
        default=None, foreign_key="unit.id", ondelete="CASCADE", unique=True, nullable=False
    )
    general_seats: str | None = None
    quota_breakdown: str | None = None
    unit: Unit = Relationship(back_populates="seat_info")


class ImportantDate(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    unit_id: int | None = Field(
        default=None, foreign_key="unit.id", ondelete="CASCADE", unique=True, nullable=False
    )
    application_start: date | None = None
    application_end: date | None = None
    admit_card_start: date | None = None
    exam_date: date | None = None
    unit: Unit = Relationship(back_populates="important_date")


class FeeStructure(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    unit_id: int | None = Field(
        default=None, foreign_key="unit.id", ondelete="CASCADE", unique=True, nullable=False
    )
    application_fee: str | None = None
    payment_methods: str | None = None
    unit: Unit = Relationship(back_populates="fee_structure")
