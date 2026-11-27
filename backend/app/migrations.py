"""Migrations for existing local SQLite databases."""

from sqlalchemy import inspect
from sqlalchemy.engine import Engine


def migrate_legacy_university_schema(engine: Engine) -> None:
    if engine.dialect.name != "sqlite":
        inspector = inspect(engine)
        if inspector.has_table("unit"):
            unit_columns = {
                column["name"] for column in inspector.get_columns("unit")
            }
            if "university_id" in unit_columns and "prospectus_id" not in unit_columns:
                raise RuntimeError(
                    "Apply migrations/postgresql_split_prospectuses.sql before starting "
                    "against an existing PostgreSQL database."
                )
        return

    connection = engine.raw_connection()
    cursor = connection.cursor()
    try:
        tables = {
            row[0]
            for row in cursor.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }
        if "university" not in tables or "unit" not in tables:
            return

        unit_columns = {
            row[1] for row in cursor.execute("PRAGMA table_info('unit')")
        }
        if "university_id" not in unit_columns:
            return
        if "prospectus" in tables:
            raise RuntimeError(
                "Legacy university schema is partially migrated; manual repair is required."
            )

        university_columns = {
            row[1] for row in cursor.execute("PRAGMA table_info('university')")
        }
        if not {
            "session",
            "overview",
            "application_start",
            "application_end",
            "admit_card_download",
            "exam_date",
        }.issubset(university_columns):
            raise RuntimeError("Legacy university data is missing prospectus fields.")

        cursor.execute("PRAGMA foreign_keys = OFF")
        cursor.execute("PRAGMA legacy_alter_table = ON")
        cursor.execute("BEGIN")
        cursor.execute(
            """
            CREATE TABLE prospectus (
                id INTEGER NOT NULL PRIMARY KEY,
                university_id INTEGER NOT NULL
                    REFERENCES university(id) ON DELETE CASCADE,
                session VARCHAR(20) NOT NULL,
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
        cursor.execute(
            """
            INSERT INTO prospectus
                (id, university_id, session, overview, application_start,
                 application_end, admit_card_download, exam_date, created_at, updated_at)
            SELECT id, id, session, overview, application_start, application_end,
                   admit_card_download, exam_date, created_at, updated_at
            FROM university
            """
        )
        cursor.execute("CREATE INDEX ix_prospectus_university_id ON prospectus (university_id)")
        cursor.execute(
            """
            CREATE TABLE unit_new (
                id INTEGER NOT NULL PRIMARY KEY,
                prospectus_id INTEGER NOT NULL
                    REFERENCES prospectus(id) ON DELETE CASCADE,
                unit_name VARCHAR(120) NOT NULL,
                background VARCHAR(40) NOT NULL,
                total_seats VARCHAR
            )
            """
        )
        cursor.execute(
            """
            INSERT INTO unit_new (id, prospectus_id, unit_name, background, total_seats)
            SELECT id, university_id, unit_name, background, total_seats
            FROM unit
            """
        )
        cursor.execute("DROP TABLE unit")
        cursor.execute("ALTER TABLE unit_new RENAME TO unit")
        cursor.execute("CREATE INDEX ix_unit_prospectus_id ON unit (prospectus_id)")

        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute("PRAGMA legacy_alter_table = OFF")
        cursor.close()
        connection.close()
