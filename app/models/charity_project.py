from sqlalchemy import Column, String, Text

from app.models.base import BaseProjectModel


class CharityProject(BaseProjectModel):
    name = Column(
        String(100),
        unique=True,
        nullable=False,
    )
    description = Column(Text, nullable=False)

    def __repr__(self):
        return super().__repr__()
