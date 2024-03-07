from flask import Blueprint, request, session
from http import HTTPStatus
from database.models import Lesson, Block
from sqlalchemy import select
from database import db


lesson_creation = Blueprint("lesson", __name__, url_prefix="lesson")


@lesson_creation.route("/create/", methods=["POST"])
def create_lesson():
    if not session["user"]:
        return {"message": "User not logged in"}, HTTPStatus.UNAUTHORIZED

    title = request.form["title"]
    description = request.form["description"]
    age_rating = request.form["age_rating"]
    thumbnail = request.form["thumbnail"]
    creator_id = session["user"].id

    if not title and not description:
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

    return {"message": "Lesson successfully created"}, HTTPStatus.CREATED


@lesson_creation.route("/create-block/<int:lesson_id>", methods=["POST"])
def create_lesson_block(lesson_id: int):
    if not session["user"]:
        return {"message": "User not logged in"}, HTTPStatus.UNAUTHORIZED

    if not session["user"].id == session["lesson"].creator_id:
        return {"message": "User not authorized"}, HTTPStatus.FORBIDDEN

    lesson_type = request.form["lesson-type"]
    subtitle = request.form["subtitle"]
    content = request.form["content"]

    if not content:
        return {"message": "No input provided"}, HTTPStatus.BAD_REQUEST

    block = Block(
        lesson_id=lesson_id, type=lesson_type, subtitle=subtitle, content=content
    )

    db.session.add(block)
    db.session.commit()

    return {"message": "Lesson block successfully created"}, HTTPStatus.CREATED
