from sqlmodel import Session, SQLModel, create_engine

from app.migrations import migrate_legacy_university_schema
from app.universities.repository import UniversityRepository
from app.universities.schemas import UniversityRead


def test_legacy_sqlite_schema_migrates_university_data_to_prospectus() -> None:
    engine = create_engine("sqlite://")
    with engine.begin() as connection:
        connection.exec_driver_sql(
            """
            CREATE TABLE university (
                id INTEGER PRIMARY KEY,
                name VARCHAR(150) NOT NULL,
                session VARCHAR(20) NOT NULL,
                website_url VARCHAR(500),
                overview VARCHAR(2000) NOT NULL,
                application_start DATE,
                application_end DATE,
                admit_card_download DATE,
                exam_date DATE,
                created_at DATETIME NOT NULL,
                updated_at DATETIME NOT NULL
            )
            """
        )
        connection.exec_driver_sql(
            """
            CREATE TABLE unit (
                id INTEGER PRIMARY KEY,
                university_id INTEGER NOT NULL,
                unit_name VARCHAR(120) NOT NULL,
                background VARCHAR(40) NOT NULL,
                total_seats INTEGER,
                FOREIGN KEY(university_id) REFERENCES university(id) ON DELETE CASCADE
            )
            """
        )
        connection.exec_driver_sql(
            """
            CREATE TABLE importantdate (
                id INTEGER PRIMARY KEY,
                unit_id INTEGER NOT NULL UNIQUE,
                application_start DATE,
                application_end DATE,
                admit_card_start DATE,
                exam_date DATE,
                FOREIGN KEY(unit_id) REFERENCES unit(id) ON DELETE CASCADE
            )
            """
        )
        connection.exec_driver_sql(
            """
            INSERT INTO university
                (id, name, session, website_url, overview, application_start,
                 application_end, admit_card_download, exam_date, created_at, updated_at)
            VALUES
                (1, 'Example University', '2026-2027', 'https://example.edu',
                 'Undergraduate admission', '2026-01-01', '2026-02-01',
                 '2026-03-01', '2026-04-01', '2025-01-01', '2025-01-01')
            """
        )
        connection.exec_driver_sql(
            """
            INSERT INTO unit (id, university_id, unit_name, background, total_seats)
            VALUES (5, 1, 'A Unit', 'Science', 40)
            """
        )
        connection.exec_driver_sql(
            """
            INSERT INTO importantdate
                (id, unit_id, application_start, application_end, admit_card_start, exam_date)
            VALUES (7, 5, '2026-01-15', NULL, NULL, NULL)
            """
        )

    migrate_legacy_university_schema(engine)
    SQLModel.metadata.create_all(engine)

    with engine.connect() as connection:
        assert connection.exec_driver_sql("PRAGMA foreign_key_check('unit')").all() == []
        assert connection.exec_driver_sql(
            "PRAGMA foreign_key_check('importantdate')"
        ).all() == []

    with Session(engine) as session:
        university = UniversityRepository(session).get(1)
        assert university is not None
        response = UniversityRead.model_validate(university, from_attributes=True)

    prospectus = response.prospectuses[0]
    assert prospectus.session == "2026-2027"
    assert prospectus.overview == "Undergraduate admission"
    assert prospectus.application_start.isoformat() == "2026-01-01"
    assert prospectus.application_end.isoformat() == "2026-02-01"
    assert prospectus.admit_card_download.isoformat() == "2026-03-01"
    assert prospectus.exam_date.isoformat() == "2026-04-01"
    assert prospectus.units[0].unit_name == "A Unit"
    important_date = prospectus.units[0].important_date
    assert important_date is not None
    assert important_date.application_start.isoformat() == "2026-01-15"
