from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import BaseProjectModel


class Donation(BaseProjectModel):
    user_id = Column(
        Integer, ForeignKey('user.id', name='fk_donation_user_id_user')
    )
    comment = Column(Text, nullable=True)

    def __repr__(self):
        return super().__repr__()
