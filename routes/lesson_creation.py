from flask import Blueprint, request, session
from http import HTTPStatus
from database.models import Lesson, Block, LessonAgeEnum, BlockTypeEnum, Tag
from sqlalchemy import select
from sqlalchemy.dialects.sqlite import insert
from database import db
from uuid import uuid4
from base64 import decodebytes
from helpers import require_login

lesson_creation = Blueprint("lesson", __name__, url_prefix="/lesson")


def load_image(file_content: str, extension: str) -> str:
    file_content = file_content.encode("utf-8")
    file_content = decodebytes(file_content)
    filename = "image_" + str(uuid4()) + extension

    file = open("assets/" + filename, "wb")
    file.write(file_content)
    file.close()

    return filename


def create_lesson():
    lesson = request.json["lesson"]

    if not lesson.get("age_rating", "") in LessonAgeEnum.__members__:
        return {
            "success": False,
            "message": "No such age rating",
        }, HTTPStatus.BAD_REQUEST

    title = lesson.get("title")
    description = lesson.get("description")
    age_rating = lesson.get("age_rating")
    thumbnail = lesson.get("thumbnail")
    extension = lesson.get("extension")
    user = session["user"]
    db.session.add(user)
    creator_id = user.id
    tags = lesson.get("tags")

    if not title or not description:
        return {"success": False, "message": "Invalid input"}, HTTPStatus.BAD_REQUEST

    if thumbnail:
        if not extension:
            return {"success": False, "message": "No extension"}, HTTPStatus.BAD_REQUEST
        thumbnail = load_image(thumbnail, extension)

    lesson = Lesson(
        title=title,
        description=description,
        age_rating=age_rating,
        thumbnail=thumbnail,
        creator_id=creator_id,
    )

    db.session.add(lesson)
    db.session.commit()

    if tags:
        for tag in tags:
            db.session.execute(insert(Tag).values(tag=tag).on_conflict_do_nothing())
            resp = db.session.execute(select(Tag).where(Tag.tag == tag)).scalar()
            if resp not in lesson.tags:
                lesson.tags.append(resp)
        db.session.commit()

    for block in request.json["blocks"]:
        (message, status) = create_block(block, lesson.id)
        if not message["success"]:
            return {"success": False, "message": message["message"]}, status

    return {
        "success": True,
        "message": "Lesson successfully created",
    }, HTTPStatus.CREATED


@lesson_creation.route("/deploy/", methods=["POST"])
@require_login
def deploy_lesson():
    (message, status) = create_lesson()
    return {"message": message["message"]}, status


def create_block(_block: Block, lesson_id: int):

    if not _block.get("type", "") in BlockTypeEnum.__members__:
        return {
            "success": False,
            "message": "No such block type",
        }, HTTPStatus.BAD_REQUEST

    block_type = _block.get("type")
    subtitle = _block.get("subtitle")
    content = _block.get("content")
    extension = _block.get("extension")

    if not content:
        return {
            "success": False,
            "message": "No input provided",
        }, HTTPStatus.BAD_REQUEST

    if block_type == "IMAGE":
        if not extension:
            return {"success": False, "message": "No extension"}, HTTPStatus.BAD_REQUEST
        content = load_image(content, extension)

    block = Block(
        lesson_id=lesson_id, type=block_type, subtitle=subtitle, content=content
    )

    db.session.add(block)
    db.session.commit()

    return {
        "success": True,
        "message": "Lesson block successfully created",
    }, HTTPStatus.CREATED


@lesson_creation.route("/update/", methods=["POST"])
@require_login
def update_lesson():
    lesson = request.json["lesson"]
    old_lesson = db.session.get(Lesson, lesson.get("id"))

    if not old_lesson:
        return {"message": "No such lesson"}, HTTPStatus.BAD_REQUEST

    if not old_lesson.creator_id == session["user"].id:
        return {"message": "Not authorized"}, HTTPStatus.FORBIDDEN

    (message, status) = create_lesson()
    if not message["success"]:
        return {"message": message["message"]}, status
    db.session.delete(old_lesson)
    db.session.commit()
    return {"message": "Lesson successfully updated"}, HTTPStatus.OK


@lesson_creation.route("/delete_lesson/", methods=["POST"])
@require_login
def delete_lesson():
    lesson_id = request.json.get("lesson_id")

    if not lesson_id:
        return {"message": "No data provided"}, HTTPStatus.BAD_REQUEST

    lesson = db.session.get(Lesson, lesson_id)

    if not lesson:
        return {"message": "No such lesson"}, HTTPStatus.BAD_REQUEST

    db.session.delete(lesson)
    db.session.commit()

    return {"message": "Successfully deleted lesson"}, HTTPStatus.OK
