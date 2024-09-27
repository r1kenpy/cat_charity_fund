from sqlalchemy import Column, String, Text

from app.models.base import AbstractProjectModelForInvest


class CharityProject(AbstractProjectModelForInvest):
    name = Column(
        String(100),
        unique=True,
        nullable=False,
    )
    description = Column(Text, nullable=False)

    def __repr__(self):
        return f'{self.name=}{self.description=}' + super().__repr__()
