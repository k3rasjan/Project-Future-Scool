from database import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as sqlEnum, ForeignKey
from enum import Enum
from typing import List
from .association_tables import user_lesson


class Age(Enum):
    pegi3 = "3"
    pegi7 = "7"
    pegi12 = "12"
    pegi16 = "16"
    pegi18 = "18"


class Lesson(db.Model):
    __tablename__ = "lesson"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    age_rating: Mapped[Age] = mapped_column(sqlEnum(Age), default=Age.pegi18)
    creator_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    thumbnail: Mapped[str] = mapped_column()
    creator: Mapped["User"] = relationship(back_populates="created_lessons")
    blocks: Mapped[List["Block"]] = relationship(back_populates="lesson")
    users: Mapped[List["User"]] = relationship(
        secondary=user_lesson, back_populates="lessons"
    )


from .user import User  # noqa
from .block import Block  # noqa
