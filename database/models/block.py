from database import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as sqlEnum, ForeignKey
from enum import Enum


class BlockType(Enum):
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"


class Block(db.Model):
    __tablename__ = "block"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lesson.id"), nullable=False)
    type: Mapped[BlockType] = mapped_column(sqlEnum(BlockType), default=BlockType.TEXT)
    subtitle: Mapped[str] = mapped_column()
    content: Mapped[str] = mapped_column()
    lesson: Mapped["Lesson"] = relationship(back_populates="blocks")


from .lesson import Lesson  # noqa
