from database import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as sqlEnum, ForeignKey
from enum import Enum
from typing import List
from .association_tables import user_lesson, lesson_tag


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
    thumbnail: Mapped[str] = mapped_column(default="placeholder.png")
    views: Mapped[int] = mapped_column(default=0)
    creator: Mapped["User"] = relationship(back_populates="created_lessons")
    blocks: Mapped[List["Block"]] = relationship(
        back_populates="lesson", cascade="all, delete-orphan"
    )
    users: Mapped[List["User"]] = relationship(
        secondary=user_lesson, back_populates="lessons"
    )
    tags: Mapped[List["Tag"]] = relationship(
        secondary=lesson_tag, back_populates="lessons"
    )

    def todict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "age_rating": Age(self.age_rating).value,
            "creator_id": self.creator_id,
            "thumbnail": self.thumbnail,
            "views": self.views,
            "tags": [tag.todict() for tag in self.tags],
            "creation_date": self.creation_date,
        }


from .user import User  # noqa
from .block import Block  # noqa
from .tag import Tag  # noqa
