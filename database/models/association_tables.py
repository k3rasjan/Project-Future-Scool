from .. import db
from sqlalchemy import Table, Column, ForeignKey

user_lesson = Table(
    "user_lesson",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("lesson_id", ForeignKey("lesson.id"), primary_key=True),
)
lesson_tag = Table(
    "lesson_tag",
    db.Model.metadata,
    Column("lesson_id", ForeignKey("lesson.id"), primary_key=True),
    Column("tag_id", ForeignKey("tag.id"), primary_key=True),
)
