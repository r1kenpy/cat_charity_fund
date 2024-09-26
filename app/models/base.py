from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.db import Base


class BaseProjectModel(Base):
    __abstract__ = True
    __table_args__ = (
        CheckConstraint('full_amount >= 0'),
        CheckConstraint('full_amount >= invested_amount'),
    )

    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)

    def __repr__(self):
        return (
            f'invested_amount: {self.invested_amount};\n'
            f'full_amount: {self.full_amount};\n'
            f'fully_invested: {self.fully_invested};\n'
            f'create_date: {self.create_date};\n'
            f'close_date: {self.close_date}.'
        )
