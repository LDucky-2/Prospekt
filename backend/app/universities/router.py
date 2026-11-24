"""HTTP CRUD endpoints for public universities and protected prospectus changes."""

from fastapi import APIRouter, Depends, Request, Response

from app.universities.dependencies import ServiceDep, UniversityDep
from app.universities.models import University
from app.universities.schemas import UniversityCreate, UniversityRead, UniversityUpdate
from app.rbac.dependencies import require_permission
from app.rbac.permissions import Permission
from app.auth.dependencies import CurrentUser
from app.activity.models import ActivityAction
from app.activity.recorder import record_activity
from app.database import SessionDep

router = APIRouter(prefix="/api/v1/universities", tags=["universities"])


@router.post(
    "",
    response_model=UniversityRead,
    status_code=201,
    dependencies=[Depends(require_permission(Permission.UNIVERSITY_CREATE))],
)
def create_university(
    data: UniversityCreate,
    service: ServiceDep,
    user: CurrentUser,
    request: Request,
    session: SessionDep,
) -> University:
    # University creation is protected by the RBAC dependency and logged for admins.
    university = service.create_university(data)
    record_activity(
        session,
        ActivityAction.UNIVERSITY_CREATED,
        request=request,
        account=user,
        target_id=str(university.id),
        detail=f"Created university {university.name}",
    )
    return university


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
    user: CurrentUser,
    request: Request,
    session: SessionDep,
) -> University:
    updated = service.update_university(university, data)
    record_activity(
        session,
        ActivityAction.UNIVERSITY_UPDATED,
        request=request,
        account=user,
        target_id=str(updated.id),
        detail=f"Updated university {updated.name}",
    )
    return updated


@router.delete(
    "/{university_id}",
    status_code=204,
    dependencies=[Depends(require_permission(Permission.PROSPECTUS_DELETE))],
)
def delete_university(
    university: UniversityDep,
    service: ServiceDep,
    user: CurrentUser,
    request: Request,
    session: SessionDep,
) -> Response:
    university_name = university.name
    university_id = university.id
    service.delete_university(university)
    record_activity(
        session,
        ActivityAction.UNIVERSITY_DELETED,
        request=request,
        account=user,
        target_id=str(university_id),
        detail=f"Deleted university {university_name}",
    )
    return Response(status_code=204)
