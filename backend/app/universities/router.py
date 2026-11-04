from fastapi import APIRouter, Response

from app.universities.dependencies import ServiceDep, UniversityDep
from app.universities.models import University
from app.universities.schemas import UniversityCreate, UniversityRead, UniversityUpdate

router = APIRouter(prefix="/api/v1/universities", tags=["universities"])


@router.post("", response_model=UniversityRead, status_code=201)
def create_university(data: UniversityCreate, service: ServiceDep) -> University:
    return service.create_university(data)


@router.get("", response_model=list[UniversityRead])
def list_universities(service: ServiceDep) -> list[University]:
    return service.list_universities()


@router.get("/{university_id}", response_model=UniversityRead)
def get_university(university: UniversityDep) -> University:
    return university


@router.put("/{university_id}", response_model=UniversityRead)
def update_university(
    university: UniversityDep,
    data: UniversityUpdate,
    service: ServiceDep,
) -> University:
    return service.update_university(university, data)


@router.delete("/{university_id}", status_code=204)
def delete_university(university: UniversityDep, service: ServiceDep) -> Response:
    service.delete_university(university)
    return Response(status_code=204)
