from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import Request
import logging

from app.database import create_db_and_tables
from app.database import get_session
from app.universities.router import router as universities_router
from app.auth.router import router as auth_router
from app.admin.router import router as admin_router
from app.auth.models import AppUser, UserRole
from app.auth.security import hash_password
from app.config import settings
from app.errors import AppError

logger = logging.getLogger("prospekt")

settings.validate_production_secrets()

# Central app setup: API routes, browser security, CORS and frontend hosting are registered here.

app = FastAPI(
    title="Prospekt API",
    version="0.1.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    redoc_url=None,
)

cors_origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
if settings.FRONTEND_URL:
    cors_origins.append(settings.FRONTEND_URL.rstrip("/"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    """Add browser security headers and avoid exposing application internals."""
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    return response

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(universities_router)
create_db_and_tables()


def seed_initial_admin() -> None:
    """Create the first admin only from environment variables; no public signup exists."""
    if not settings.INITIAL_ADMIN_EMAIL or not settings.INITIAL_ADMIN_PASSWORD:
        return

    session = next(get_session())
    try:
        from sqlmodel import select

        existing = session.exec(
            select(AppUser).where(AppUser.email == settings.INITIAL_ADMIN_EMAIL.lower())
        ).first()
        if existing is None:
            session.add(
                AppUser(
                    email=settings.INITIAL_ADMIN_EMAIL.lower(),
                    name=settings.INITIAL_ADMIN_NAME,
                    password_hash=hash_password(settings.INITIAL_ADMIN_PASSWORD),
                    role=UserRole.ADMIN,
                    is_active=True,
                )
            )
            session.commit()
    finally:
        session.close()


seed_initial_admin()


@app.exception_handler(AppError)
async def app_error(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(Exception)
async def unhandled_error(request: Request, exc: Exception) -> JSONResponse:
    logger.error("Unhandled error on %s %s", request.method, request.url.path, exc_info=exc)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend" / "dist"

if FRONTEND_DIR.is_dir():
    app.frontend("/", directory=FRONTEND_DIR)
