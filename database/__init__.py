from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    def todict(self):
        return {"message": "No todict method on this object class"}


db = SQLAlchemy(model_class=Base)

import database.models  # noqa
