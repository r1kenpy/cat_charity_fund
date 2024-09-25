from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_name_duplicate,
    check_investment_or_closed_project,
    check_project_exists,
    check_investment_sum,
    check_project_closed,
)
from app.core.user import current_superuser
from app.models import User
from app.schemas.charity_project import ProjectDB, ProjectCreate, ProjectUpdate
from app.core.db import get_async_session
from app.crud.charity_project import project_crud
from app.services.investing import investing

router = APIRouter()

GET_ALL_CHARITY_DESCRIPTION = (
    'Получение списка всех проектов по сбору денег для котиков'
)


@router.get(
    '/',
    response_model=list[ProjectDB],
    response_model_exclude_none=True,
    description=GET_ALL_CHARITY_DESCRIPTION,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    all_projects = await project_crud.get_multi(session=session)
    return all_projects


@router.post(
    '/',
    response_model=ProjectDB,
    response_model_exclude_none=True,
)
async def create_charity_project(
    project_data: ProjectCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser),
):
    """Только для суперюзеров."""

    await check_name_duplicate(project_name=project_data.name, session=session)
    db_project = await project_crud.create(
        session=session, obj_data=project_data
    )
    await investing(session, db_project)
    return db_project


@router.delete(
    '/{project_id}',
    response_model=ProjectDB,
    response_model_exclude_none=True,
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser),
):
    """Только для суперюзеров."""
    await check_project_exists(project_id=project_id, session=session)
    await check_investment_or_closed_project(project_id, session=session)
    project_in_db = await project_crud.get(obj_id=project_id, session=session)
    project_in_db = await project_crud.remove(
        session=session, db_obj=project_in_db
    )
    return project_in_db


@router.patch(
    '/{project_id}',
    response_model=ProjectDB,
    response_model_exclude_none=True,
)
async def update_charity_project(
    project_id: int,
    project_new_data: ProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser),
):
    """Только для суперюзеров."""
    await check_project_exists(project_id=project_id, session=session)
    await check_project_closed(project_id=project_id, session=session)
    new_project_name = project_new_data.name
    if new_project_name:
        await check_name_duplicate(
            project_name=new_project_name, session=session
        )

    new_project_amount = project_new_data.full_amount
    if new_project_amount:
        await check_investment_sum(
            project_id=project_id, session=session, obj_data=new_project_amount
        )
    project_in_db = await project_crud.get(obj_id=project_id, session=session)
    updated_project_in_db = await project_crud.update(
        session=session, obj_in=project_new_data, db_obj=project_in_db
    )

    return updated_project_in_db
