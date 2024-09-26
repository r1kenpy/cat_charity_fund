from typing import Optional

from sqlalchemy import false, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
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

    async def get_all_projects_for_invest(self, session: AsyncSession):
        projects_for_invest = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested == false()
            )
        )
        return projects_for_invest.scalars().all()


project_crud = CRUDProject(CharityProject)
