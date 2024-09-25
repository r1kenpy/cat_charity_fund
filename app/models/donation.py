from sqlalchemy import (
    Column,
    Integer,
    Text,
    ForeignKey,
)

from app.core.db import Base, MixinForInvestedProject


class Donation(Base, MixinForInvestedProject):
    user_id = Column(
        Integer, ForeignKey('user.id', name='fk_donation_user_id_user')
    )
    comment = Column(Text, nullable=True)
