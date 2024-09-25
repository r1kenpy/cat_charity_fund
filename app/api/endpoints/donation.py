from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.models import User
from app.schemas.donation import DonationDB, DonationCreate, DonationUser
from app.crud.donation import donation_crud
from app.services.investing import investing

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser),
):
    """Только для суперюзеров."""
    all_danations = await donation_crud.get_multi(session)
    return all_danations


@router.post(
    '/', response_model=DonationUser, response_model_exclude_none=True
)
async def create_donation(
    donation_obj: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    donation = await donation_crud.create(
        session=session, obj_data=donation_obj, user=user
    )
    await investing(session, donation)
    return donation


@router.get(
    '/my',
    response_model=list[DonationUser],
    response_model_exclude_none=True,
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    db_donations = await donation_crud.get_user_donations(
        session=session, user=user
    )
    return db_donations
