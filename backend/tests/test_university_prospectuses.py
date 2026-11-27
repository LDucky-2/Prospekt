from sqlmodel import Session, SQLModel, create_engine

from app.universities.models import University
from app.universities.repository import UniversityRepository
from app.universities.schemas import (
    ProspectusCreate,
    ProspectusRead,
    UniversityCreate,
    UniversityRead,
)
from app.universities.service import UniversityService


def test_university_contains_multiple_prospectuses_with_nested_units() -> None:
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        service = UniversityService(UniversityRepository(session))
        university = service.create_university(
            UniversityCreate(name="Example University", website_url="https://example.edu")
        )
        assert UniversityRead.model_validate(
            university, from_attributes=True
        ).prospectuses == []

        created_prospectus = service.create_prospectus(
            university,
            ProspectusCreate(
                session="2026-2027",
                overview="Undergraduate admission",
                application_start="2026-01-01",
                units=[
                    {
                        "unit_name": "A Unit",
                        "background": "Science",
                        "important_date": {"application_start": "2026-01-01"},
                    }
                ],
            ),
        )
        assert ProspectusRead.model_validate(
            created_prospectus, from_attributes=True
        ).units[0].unit_name == "A Unit"
        service.create_prospectus(
            university,
            ProspectusCreate(session="2027-2028", overview="Next admission cycle"),
        )

        loaded = UniversityRepository(session).get(university.id)
        assert loaded is not None
        response = UniversityRead.model_validate(loaded, from_attributes=True)

        assert response.name == "Example University"
        assert [item.session for item in response.prospectuses] == ["2026-2027", "2027-2028"]
        assert response.prospectuses[0].units[0].unit_name == "A Unit"
        assert response.prospectuses[0].application_start.isoformat() == "2026-01-01"
        assert response.prospectuses[0].units[0].important_date.application_start.isoformat() == "2026-01-01"
