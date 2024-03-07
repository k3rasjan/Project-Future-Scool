from database import db
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Tag(db.Model):
    __tablename__ = "tag"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tag: Mapped[str] = mapped_column()
