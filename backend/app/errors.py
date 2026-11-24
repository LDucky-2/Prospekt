from fastapi import HTTPException


class AppError(HTTPException):
    """Base application error that keeps HTTP status and client messages consistent."""

    def __init__(self, status_code: int, detail: str) -> None:
        super().__init__(status_code=status_code, detail=detail)
