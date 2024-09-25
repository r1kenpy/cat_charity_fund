# # DONATION
# # full_amount — сумма пожертвования, целочисленное поле; больше 0;
# # invested_amount — сумма из пожертвования, которая распределена по проектам;
# # значение по умолчанию равно 0;
# # fully_invested — булево значение, указывающее на то,
# # все ли деньги из пожертвования были переведены в тот или иной проект; по умолчанию равно False;
#
#
# # CHARITYPROJECT
# # full_amount — требуемая сумма, целочисленное поле; больше 0;
# # invested_amount — внесённая сумма, целочисленное поле; значение по умолчанию — 0;
# # fully_invested — булево значение, указывающее на то,
# # собрана ли нужная сумма для проекта (закрыт ли проект); значение по умолчанию — False;
#
# # Если full_amount из DONATION == invested_amount, то fully_invested = true, т.к
# # всю сумму зачли как пожертвование иначе остается false.
# # Выгружать можно все пожертвования можно списком, потом по нему проходиться
# # и заносить сумму в проекты.
#
# # Проверкаб что список проектов для инвестирования != 0.
# # Выружаем через из CHARITYPROJECT fully_invested == false
from datetime import datetime
import asyncio
from typing import AsyncIterator

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Donation, CharityProject


# async def get_donations(session: AsyncSession):
#
#     aaa = await session.execute(
#         select(Donation).where(Donation.fully_invested == False)
#     )
#     yield aaa.scalars()


async def ddd(session: AsyncSession, project) -> None:
    all_projects_for_invest = await session.execute(
        select(CharityProject).where(CharityProject.fully_invested == False)
    )
    all_projects_for_invest = all_projects_for_invest.scalars().all()
    if all_projects_for_invest:
        all_not_distributed_donations = await session.execute(
            select(Donation).where(Donation.fully_invested == False)
        )
        all_not_distributed_donations = (
            all_not_distributed_donations.scalars().all()
        )

        for project in all_projects_for_invest:
            # Сумма нужная для закрытия проекта
            required_amount = project.full_amount
            invested_amount_in_project = project.invested_amount
            need_sum_for_project = (
                project.full_amount - project.invested_amount
            )
            project_data = {}
            # тут же будут повторятся раз за разом уже зачисленные проекты. нужна доп проверка.
            # вомзожно тут нужно повторно делать запро на извлечения данных из бД
            for donat in all_not_distributed_donations:
                if need_sum_for_project == 0:
                    break

                donate_data = {}
                # В ДОНАТАХ
                # full_amount - не меняется
                # invested_amount - меняется
                # ранизу котрую нужно зачислить в след проект нужно вычилсять на лету
                undistributed_amount = (
                    donat.full_amount - donat.invested_amount
                )  # не распределенные донаты
                # print('undistributed_amount', undistributed_amount)
                # ------------------------------------------------------------
                # Если требуемая сумма для проекта меньше чем есть в донате
                if need_sum_for_project < undistributed_amount:
                    undistributed_amount -= need_sum_for_project
                    # print('need_sum_for_project', need_sum_for_project)
                    donate_data['invested_amount'] = (
                        donat.invested_amount + need_sum_for_project
                    )
                    project_data['invested_amount'] = (
                        project.invested_amount + need_sum_for_project
                    )
                    project_data['fully_invested'] = True
                    need_sum_for_project = 0
                elif need_sum_for_project > undistributed_amount:
                    donate_data['invested_amount'] = donat.full_amount
                    donate_data['fully_invested'] = True
                    donate_data['close_date'] = datetime.now()
                    project_data['invested_amount'] = (
                        invested_amount_in_project + undistributed_amount
                    )
                    need_sum_for_project -= undistributed_amount
                else:
                    donate_data['invested_amount'] = donat.full_amount
                    donate_data['fully_invested'] = True
                    donate_data['close_date'] = datetime.now()
                    project_data['invested_amount'] = (
                        project.invested_amount + need_sum_for_project
                    )
                    need_sum_for_project = 0

                print('donate_data', donate_data)
                # Требуемая сумма больше, чем есть в донате
                # if required_amount > undistributed_amount:
                #     required_amount -= undistributed_amount
                #     print('required_amount', required_amount)
                #     donate_data['invested_amount'] = (
                #         project.invested_amount + undistributed_amount
                #     )
                # elif required_amount == undistributed_amount:
                #     donate_data['invested_amount'] = donat.full_amount
                #     donate_data['fully_invested'] = True
                # else:
                #     donation_amount = undistributed_amount - required_amount
                #     print('donation_amount', donation_amount)
                #     required_amount = 0
                #     donate_data['invested_amount'] = donation_amount
                #     project_data['invested_amount'] = donation_amount

                for field in donate_data:
                    setattr(donat, field, donate_data[field])
                session.add(donat)
            if need_sum_for_project == 0:
                project_data['fully_invested'] = True
                project_data['close_date'] = datetime.now()

            print('project_data', project_data)
            for field in project_data:
                setattr(project, field, project_data[field])
            session.add(project)

            await session.commit()
            await session.refresh(project)
            return project
    # ?????? не понимаю как рефрешить несколько обьектов,
    # вроде это позволительно, но тогда их нужно както собирать в список.


# нужно формировать словарь, с ключами(колонками в таблице) и значением
# потом через сетаттр передавать в сессию измененные данные.
# Сумма пожертвования равна сумме
# Суммы пожертвования хватило закрыть проект
# Суммы пожертвования не хватило закрыть проект
# Сумма пожертвования больше чему нужно проекту
#
#
#
#
