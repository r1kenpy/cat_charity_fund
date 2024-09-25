from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select

from app.crud.base import CRUDBase

from sqlalchemy.ext.asyncio import AsyncSession
from app.models import CharityProject
from app.schemas.charity_project import ProjectCreate, ProjectDB


class CRUDProject(CRUDBase[CharityProject, ProjectCreate, ProjectDB]):

    async def get_project_by_name(
        self, session: AsyncSession, project_name
    ) -> Optional[CharityProject]:
        project_id = await session.execute(
            select(self.model.id).where(self.model.name == project_name)
        )
        project_id = project_id.scalars().first()
        return project_id

    async def update(
        self, session: AsyncSession, db_obj, obj_in
    ) -> CharityProject:
        obj_data = jsonable_encoder(db_obj)
        update_obj_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_obj_data:
                setattr(db_obj, field, update_obj_data[field])

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(self, session: AsyncSession, db_obj) -> CharityProject:
        await session.delete(db_obj)
        await session.commit()
        return db_obj


project_crud = CRUDProject(CharityProject)
