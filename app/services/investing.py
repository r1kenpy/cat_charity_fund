from datetime import datetime
from typing import List

from app.models.base import BaseProjectModel


async def investing(
    target: BaseProjectModel,
    sources: List[BaseProjectModel],
):
    updated_objects = []
    if target.invested_amount is None:
        target.invested_amount = 0
    for source in sources:
        need_sum_for_invest = target.full_amount - target.invested_amount
        for obj in (target, source):
            obj.invested_amount += need_sum_for_invest
            if obj.invested_amount == obj.full_amount:
                obj.fully_invested = True
                obj.close_date = datetime.now()
        updated_objects.append(obj)

        if target.fully_invested:
            break

    return updated_objects
