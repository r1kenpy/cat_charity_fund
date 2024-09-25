from datetime import datetime
from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Donation, CharityProject


async def get_objects_from_models(session: AsyncSession):
    projects_for_invest = await session.execute(
        select(CharityProject).where(CharityProject.fully_invested == False)
    )
    projects_for_invest = projects_for_invest.scalars().all()

    not_distributed_donations = await session.execute(
        select(Donation).where(Donation.fully_invested == False)
    )
    not_distributed_donations = not_distributed_donations.scalars().all()

    return projects_for_invest, not_distributed_donations


async def close_object(object_model: Union[Donation, CharityProject]) -> None:
    object_model.invested_amount = object_model.full_amount
    object_model.fully_invested = True
    object_model.close_date = datetime.now()


async def investing(
    session: AsyncSession, object_model: Union[Donation, CharityProject]
) -> Union[Donation, CharityProject]:
    projects_for_invest, not_distributed_donations = (
        await get_objects_from_models(session)
    )
    if not projects_for_invest or not not_distributed_donations:
        return object_model
    else:
        for project in projects_for_invest:
            need_sum_for_project = (
                project.full_amount - project.invested_amount
            )
            for donat in not_distributed_donations:
                undistributed_amount = (
                    donat.full_amount - donat.invested_amount
                )
                if need_sum_for_project < undistributed_amount:
                    undistributed_amount -= need_sum_for_project
                    donat.invested_amount += need_sum_for_project
                    project.invested_amount += need_sum_for_project
                    await close_object(project)
                elif need_sum_for_project > undistributed_amount:
                    await close_object(donat)
                    project.invested_amount += undistributed_amount
                    need_sum_for_project -= undistributed_amount
                else:
                    await close_object(donat)
                    project.invested_amount = need_sum_for_project
                    await close_object(project)

                session.add(donat)
                session.add(project)
                if project.invested_amount == project.full_amount:
                    break
        await session.commit()
        await session.refresh(object_model)
        return object_model
