from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation
from app.schemas.donation import DonationCreate, DonationDB, DonationUser
from app.models import User


class CRUDDonation(CRUDBase[Donation, DonationCreate, DonationDB]):

    async def get_user_donations(
        self, session: AsyncSession, user: User
    ) -> List[DonationDB]:
        obj_in_db = await session.execute(
            select(self.model).where(self.model.user_id == user.id)
        )
        return obj_in_db.scalars().all()


donation_crud = CRUDDonation(Donation)
