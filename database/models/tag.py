from database import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from .association_tables import lesson_tag


class Tag(db.Model):
    __tablename__ = "tag"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tag: Mapped[str] = mapped_column(unique=True)
    lessons: Mapped[List["Lesson"]] = relationship(
        secondary=lesson_tag, back_populates="tags"
    )

    def todict(self):
        return {"id": self.id, "tag": self.tag}


from .lesson import Lesson  # noqa
