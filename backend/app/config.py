from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parent.parent
_UNSUPPORTED_QUERY_KEYS = {"supa", "pgbouncer"}


def _to_sqlalchemy_url(url: str) -> str:
    if not url.startswith(("postgres://", "postgresql://", "postgresql+psycopg://")):
        return url

    url = "postgresql+psycopg://" + url.split("://", 1)[1]
    parts = urlsplit(url)
    query = [(key, value) for key, value in parse_qsl(parts.query) if key not in _UNSUPPORTED_QUERY_KEYS]
    return urlunsplit(parts._replace(query=urlencode(query)))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BACKEND_DIR / ".env", extra="ignore")

    DATABASE_URL: str | None = None
    POSTGRES_URL: str | None = None
    VERCEL: str | None = None

    @property
    def database_url(self) -> str:
        url = self.DATABASE_URL or self.POSTGRES_URL
        if url:
            return _to_sqlalchemy_url(url)

        db_dir = Path("/tmp") if self.VERCEL else BACKEND_DIR
        return f"sqlite:///{(db_dir / 'prospekt.db').as_posix()}"


settings = Settings()
