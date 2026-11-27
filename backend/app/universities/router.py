"""HTTP CRUD endpoints for public universities and protected prospectus changes."""

from fastapi import APIRouter, Depends, HTTPException, Request, Response

from app.universities.dependencies import ServiceDep, UniversityDep
from app.universities.models import Prospectus, University
from app.universities.schemas import (
    ProspectusCreate,
    ProspectusRead,
    ProspectusUpdate,
    UniversityCreate,
    UniversityRead,
    UniversityUpdate,
)
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


@router.post(
    "/{university_id}/prospectuses",
    response_model=ProspectusRead,
    status_code=201,
    dependencies=[Depends(require_permission(Permission.PROSPECTUS_CREATE))],
)
def create_prospectus(
    university: UniversityDep,
    data: ProspectusCreate,
    service: ServiceDep,
    user: CurrentUser,
    request: Request,
    session: SessionDep,
) -> Prospectus:
    prospectus = service.create_prospectus(university, data)
    record_activity(
        session,
        ActivityAction.PROSPECTUS_CREATED,
        request=request,
        account=user,
        target_id=str(university.id),
        detail=f"Created prospectus for {university.name}, session {prospectus.session}",
    )
    return prospectus


@router.put(
    "/{university_id}/prospectuses/{prospectus_id}",
    response_model=ProspectusRead,
    dependencies=[Depends(require_permission(Permission.PROSPECTUS_UPDATE))],
)
def update_prospectus(
    university_id: int,
    university: UniversityDep,
    prospectus_id: int,
    data: ProspectusUpdate,
    service: ServiceDep,
    user: CurrentUser,
    request: Request,
    session: SessionDep,
) -> Prospectus:
    prospectus = service.get_prospectus(university_id, prospectus_id)
    if prospectus is None:
        raise HTTPException(status_code=404, detail="Prospectus not found")
    updated = service.update_prospectus(prospectus, data)
    record_activity(
        session,
        ActivityAction.PROSPECTUS_UPDATED,
        request=request,
        account=user,
        target_id=str(university.id),
        detail=f"Updated prospectus for {university.name}, session {updated.session}",
    )
    return updated


@router.delete(
    "/{university_id}/prospectuses/{prospectus_id}",
    status_code=204,
    dependencies=[Depends(require_permission(Permission.PROSPECTUS_DELETE))],
)
def delete_prospectus(
    university_id: int,
    university: UniversityDep,
    prospectus_id: int,
    service: ServiceDep,
    user: CurrentUser,
    request: Request,
    session: SessionDep,
) -> Response:
    prospectus = service.get_prospectus(university_id, prospectus_id)
    if prospectus is None:
        raise HTTPException(status_code=404, detail="Prospectus not found")
    prospectus_session = prospectus.session
    service.delete_prospectus(prospectus)
    record_activity(
        session,
        ActivityAction.PROSPECTUS_DELETED,
        request=request,
        account=user,
        target_id=str(university.id),
        detail=f"Deleted prospectus for {university.name}, session {prospectus_session}",
    )
    return Response(status_code=204)
