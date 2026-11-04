from typing import Annotated

from fastapi import Depends, HTTPException

from app.database import SessionDep
from app.universities.models import University
from app.universities.repository import UniversityRepository
from app.universities.service import UniversityService


def get_university_service(session: SessionDep) -> UniversityService:
    return UniversityService(UniversityRepository(session))


ServiceDep = Annotated[UniversityService, Depends(get_university_service)]


def valid_university(university_id: int, service: ServiceDep) -> University:
    university = service.get_university(university_id)
    if university is None:
        raise HTTPException(status_code=404, detail="University not found")
    return university


UniversityDep = Annotated[University, Depends(valid_university)]
