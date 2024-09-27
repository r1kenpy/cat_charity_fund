from datetime import datetime
from typing import List

from app.models.base import AbstractProjectModelForInvest


def investing(
    target: AbstractProjectModelForInvest,
    sources: List[AbstractProjectModelForInvest],
):
    updated = []
    for source in sources:
        need_sum_for_invest = min(
            source.full_amount - source.invested_amount,
            target.full_amount - target.invested_amount,
        )
        for obj in (target, source):
            obj.invested_amount += need_sum_for_invest
            if obj.invested_amount == obj.full_amount:
                obj.fully_invested = True
                obj.close_date = datetime.now()
        updated.append(obj)

        if target.fully_invested:
            break

    return updated
