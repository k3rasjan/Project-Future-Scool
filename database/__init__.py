from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from sqlalchemy import DateTime, func
from abc import abstractmethod


class Base(DeclarativeBase):
    creation_date: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    @abstractmethod
    def todict(self):
        raise NotImplementedError


db = SQLAlchemy(model_class=Base)

import database.models  # noqa
