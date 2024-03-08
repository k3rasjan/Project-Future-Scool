from flask import Blueprint, request, session
from http import HTTPStatus
from database.models import Lesson, Block, LessonAgeEnum, BlockTypeEnum
from database import db


lesson_creation = Blueprint("lesson", __name__, url_prefix="/lesson")


@lesson_creation.route("/create/", methods=["POST"])
def create_lesson():
    if not session["user"]:
        return {"message": "User not logged in"}, HTTPStatus.UNAUTHORIZED

    lesson = request.json["lesson"]

    if not lesson.get("age_rating", "") in LessonAgeEnum.__members__:
        return {"message": "No such age rating"}, HTTPStatus.BAD_REQUEST

    title = lesson.get("title")
    description = lesson.get("description")
    age_rating = lesson.get("age_rating")
    thumbnail = lesson.get("thumbnail")
    creator_id = session["user"].id

    if not title or not description:
        return {"message": "Invalid input"}, HTTPStatus.BAD_REQUEST

    lesson = Lesson(
        title=title,
        description=description,
        age_rating=age_rating,
        thumbnail=thumbnail,
        creator_id=creator_id,
    )

    db.session.add(lesson)
    db.session.commit()

    for block in request.json["blocks"]:
        create_block(block, lesson.id)

    return {"message": "Lesson successfully created"}, HTTPStatus.CREATED


def create_block(_block: Block, lesson_id: int):

    if not _block.get("type", "") in BlockTypeEnum.__members__:
        return {"message": "No such block type"}, HTTPStatus.BAD_REQUEST

    block_type = BlockTypeEnum[_block.get("type")]
    subtitle = _block.get("subtitle")
    content = _block.get("content")

    if not content:
        return {"message": "No input provided"}, HTTPStatus.BAD_REQUEST

    block = Block(
        lesson_id=lesson_id, type=block_type, subtitle=subtitle, content=content
    )

    db.session.add(block)
    db.session.commit()

    return {"message": "Lesson block successfully created"}, HTTPStatus.CREATED


@lesson_creation.route("/update/", methods=["POST"])
def update_lesson():
    lesson = request.json["lesson"]
    old_lesson = db.session.get(Lesson, lesson.get("id"))

    if not old_lesson:
        return {"message": "No such lesson"}, HTTPStatus.BAD_REQUEST

    if not old_lesson.creator_id == session["user"].id:
        return {"message": "Not authorized"}, HTTPStatus.FORBIDDEN

    db.session.delete(old_lesson)
    db.session.commit()
    create_lesson()
