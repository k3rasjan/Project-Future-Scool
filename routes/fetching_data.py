from http import HTTPStatus
from flask import Blueprint, request, session
from sqlalchemy import select, update
from database import db
from database.models import Lesson, Block, user_lesson, lesson_tag, User, Tag
from helpers import require_login

fetching_data = Blueprint("fetching_data", __name__, url_prefix="/fetching_data")


@fetching_data.route("/get_lesson/", methods=["GET"])
@require_login
def get_lesson():

    lesson_id = request.json["lesson_id"]
    user = session["user"]
    lesson = db.session.get(Lesson, lesson_id)

    if not lesson:
        return {"message": "Lesson not found"}, HTTPStatus.NOT_FOUND

    resp = db.session.execute(select(Block).where(Block.lesson_id == lesson_id))

    blocks = []

    for block in resp:
        blocks.append(block[0].todict())

    if user not in lesson.users:
        lesson.users.append(user)

    db.session.execute(
        update(Lesson).where(Lesson.id == lesson_id).values({"views": Lesson.views + 1})
    )
    db.session.commit()

    return {
        "lesson": lesson.todict(),
        "blocks": [blocks],
    }, HTTPStatus.OK


@fetching_data.route("/get_lessons_by_views/", methods=["GET"])
def get_lessons_by_views():
    lessons = []
    response = db.session.execute(select(Lesson).limit(15))
    for lesson in response:
        lessons.append(lesson[0].todict())

    if len(lessons) == 0:
        return {"message": "No lessons found"}, HTTPStatus.NOT_FOUND

    return {"lessons": lessons}, HTTPStatus.OK


@fetching_data.route("/get_user_lessons", methods=["GET"])
@require_login
def get_user_lessons():
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


@fetching_data.route("/get_lessons_by_tags/", methods=["GET"])
def get_lessons_by_tags():
    lessons = {}
    tags = []
    tag_response = db.session.execute(select(Tag))
    for tag in tag_response:
        tags.append(tag[0])

    for tag in tags:
        response = db.session.execute(
            select(Lesson).join(lesson_tag).join(Tag).where(Tag.id == tag.id)
        )

        lessons[tag.tag] = []

        for lesson in response:
            lessons[tag.tag].append(lesson[0].todict())
    return {"lessons": lessons}, HTTPStatus.OK


@fetching_data.route("/created_lessons/", methods=["GET"])
@require_login
def get_created_lessons():
    user = session.get("user")
    db.session.add(user)
    lessons = [lesson.todict() for lesson in user.created_lessons]

    return {"lessons": lessons}, HTTPStatus.OK


@fetching_data.route("/user_data/", methods=["GET"])
@require_login
def get_user_data():
    user = session.get("user")
    db.session.add(user)
    return {"user_data": user.todict()}, HTTPStatus.OK


@fetching_data.route("/search_lesson/", methods=["GET"])
def search_lesson():
    phrase = str(request.json.get("phrase")).casefold().replace(" ", "")
    lessons = db.session.scalars(select(Lesson)).all()
    results = []

    for lesson in lessons:
        if lesson.title.casefold().replace(" ", "").find(phrase) != -1:
            results.append(lesson.todict())
        elif lesson.description.casefold().replace(" ", "").find(phrase) != -1:
            results.append(lesson.todict())

    return {"lessons": results}, HTTPStatus.OK


@fetching_data.route("/search_tag/", methods=["GET"])
def search_tag():
    phrase = str(request.json.get("phrase"))
    tags = db.session.query(Tag).all()
    results = []
    for tag in tags:
        if tag.tag.find(phrase) != -1:
            results.append(tag.todict())

    return {"tags": results}, HTTPStatus.OK


@fetching_data.route("/get_creator_name/", methods=["GET"])
def get_creator_name():
    creator_id = request.json.get("creator_id")
    user = db.session.query(User).where(User.id == creator_id).first()
    user_name = user.username
    if not user:
        return {"message": "Creator not found"}, HTTPStatus.BAD_REQUEST
    return {"creator_name": user_name}, HTTPStatus.OK
