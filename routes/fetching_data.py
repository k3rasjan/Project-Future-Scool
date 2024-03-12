from http import HTTPStatus
from flask import Blueprint, request, session
from sqlalchemy import select
from database import db
from database.models import Lesson, Block
from database.models import LessonAgeEnum

fetching_data = Blueprint("fetching_data", __name__, url_prefix="/fetching_data")


@fetching_data.route("/get_lesson/", methods=["GET"])
def get_lesson():
    lesson_id = request.json["lesson_id"]
    lesson = db.session.get(Lesson, lesson_id)

    if not lesson:
        return {"message": "Lesson not found"}, HTTPStatus.NOT_FOUND

    blocks = db.session.execute(select(Block).where(Block.lesson_id == lesson_id))

    print(lesson.age_rating)

    return {
        "lesson": {
            "id": lesson.id,
            "title": lesson.title,
            "description": lesson.description,
            "age_rating": LessonAgeEnum[lesson.age_rating],
            "creator_id": lesson.creator_id,
        }
    }, HTTPStatus.OK
