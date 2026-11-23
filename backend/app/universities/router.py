from fastapi import APIRouter, Depends, Response

from app.universities.dependencies import ServiceDep, UniversityDep
from app.universities.models import University
from app.universities.schemas import UniversityCreate, UniversityRead, UniversityUpdate
from app.rbac.dependencies import require_permission
from app.rbac.permissions import Permission

router = APIRouter(prefix="/api/v1/universities", tags=["universities"])


@router.post(
    "",
    response_model=UniversityRead,
    status_code=201,
    dependencies=[Depends(require_permission(Permission.UNIVERSITY_CREATE))],
)
def create_university(data: UniversityCreate, service: ServiceDep) -> University:
    return service.create_university(data)


@router.get("", response_model=list[UniversityRead])
def list_universities(service: ServiceDep) -> list[University]:
    return service.list_universities()


@router.get("/{university_id}", response_model=UniversityRead)
def get_university(university: UniversityDep) -> University:
    return university


@router.put(
    "/{university_id}",
    response_model=UniversityRead,
    dependencies=[Depends(require_permission(Permission.PROSPECTUS_UPDATE))],
)
def update_university(
    university: UniversityDep,
    data: UniversityUpdate,
    service: ServiceDep,
) -> University:
    return service.update_university(university, data)


@router.delete(
    "/{university_id}",
    status_code=204,
    dependencies=[Depends(require_permission(Permission.PROSPECTUS_DELETE))],
)
def delete_university(university: UniversityDep, service: ServiceDep) -> Response:
    service.delete_university(university)
    return Response(status_code=204)
