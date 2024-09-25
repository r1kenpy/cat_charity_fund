from sqlalchemy import Column, String, Text

from app.core.db import Base, MixinForInvestedProject


class CharityProject(Base, MixinForInvestedProject):
    name = Column(
        String(100),
        unique=True,
        nullable=False,
    )
    description = Column(Text, nullable=False)
