from http import HTTPStatus
from flask import Blueprint, request, session
from sqlalchemy import select, update
from sqlalchemy.dialects.sqlite import insert
from database import db
from database.models import Lesson, Block, user_lesson, lesson_tag, User
from database.models import LessonAgeEnum, BlockTypeEnum

fetching_data = Blueprint("fetching_data", __name__, url_prefix="/fetching_data")


@fetching_data.route("/get_lesson/", methods=["GET"])
def get_lesson():
    if not session["user"]:
        return {
            "message": "User not logged in",
        }, HTTPStatus.UNAUTHORIZED

    lesson_id = request.json["lesson_id"]
    user_id = session["user"].id
    lesson = db.session.get(Lesson, lesson_id)

    if not lesson:
        return {"message": "Lesson not found"}, HTTPStatus.NOT_FOUND

    resp = db.session.execute(select(Block).where(Block.lesson_id == lesson_id))

    blocks = []

    for block in resp:
        blocks.append(block[0].todict())

    db.session.execute(
        insert(user_lesson)
        .values(user_id=user_id, lesson_id=lesson_id)
        .on_conflict_do_nothing()
    )
    db.session.execute(
        update(Lesson).where(Lesson.id == lesson_id).values({"views": Lesson.views + 1})
    )
    db.session.commit()

    return {
        "lesson": lesson.todict(),
        "blocks": [blocks],
    }, HTTPStatus.OK


@fetching_data.route("/get_lessons/", methods=["GET"])
def get_lessons_by_views():
    lessons = []
    response = db.session.execute(select(Lesson).limit(15))
    for lesson in response:
        lessons.append(lesson[0].todict())

    if len(lessons) == 0:
        return {"message": "No lessons found"}, HTTPStatus.NOT_FOUND

    return {"lessons": [lessons]}, HTTPStatus.OK


@fetching_data.route("/get_user_lessons")
def get_user_lessons():
    if not session["user"]:
        return {
            "message": "User not logged in",
        }, HTTPStatus.UNAUTHORIZED
    user_lessons = []
    user_id = session["user"].id
    response = db.session.execute(
        select(Lesson).join(user_lesson).join(User).where(User.id == user_id)
    )

    for lesson in response:
        user_lessons.append(lesson[0].todict())

    if len(user_lessons) == 0:
        return {"message": "No lessons found"}, HTTPStatus.NOT_FOUND

    return {"user_lessons": [user_lessons]}, HTTPStatus.OK
