from database import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from typing import List
from .association_tables import user_lesson


class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    username: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    date_of_birth: Mapped[date]
    created_lessons: Mapped[List["Lesson"]] = relationship(back_populates="creator")
    lessons: Mapped[List["Lesson"]] = relationship(
        secondary=user_lesson, back_populates="users"
    )


from .lesson import Lesson  # noqa
