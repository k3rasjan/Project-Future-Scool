from flask import Blueprint, request, session, jsonify
from http import HTTPStatus
from database.models import User
from sqlalchemy import select, or_
from hashlib import sha256
from uuid import uuid4
from database import db
from datetime import date
from helpers import require_login
from flask_cors import CORS

authentication = Blueprint("authentication", __name__)


@authentication.route("/register/", methods=["POST"])
def register():
    username = request.json["username"]
    password = request.json["password"]
    password_confirmation = request.json["password-confirmation"]
    email = request.json["email"]
    date_of_birth = date.fromisoformat(request.json["date-of-birth"])

    if (
        not username
        or not password
        or not password_confirmation
        or not email
        or not date_of_birth
    ):
        return {"message": "Missing fields"}, HTTPStatus.BAD_REQUEST

    if password != password_confirmation:
        message = {"message": "Password does not match password-confirmation"}
        return message, HTTPStatus.BAD_REQUEST

    existing_user = db.session.execute(
        select(User).where(or_(User.username == username, User.email == email))
    ).scalar()

    if existing_user:
        return {"message": "User already exists"}, HTTPStatus.BAD_REQUEST

    salt = str(uuid4()).encode("utf-8")

    password = password.encode("utf-8")

    new_user = User(
        username=username,
        email=email,
        password=sha256(password + salt).hexdigest(),
        salt=salt,
        date_of_birth=date_of_birth,
    )

    db.session.add(new_user)
    db.session.commit()
    return {"message": "Successfully registered!"}, HTTPStatus.CREATED


@authentication.route("/login/", methods=["POST"])
def login_user():
    login = request.json["login"]
    password = request.json["password"]

    if not login or not password:
        return {"message": "Missing credentials"}, HTTPStatus.BAD_REQUEST

    user = db.session.execute(
        select(User).where(or_(User.username == login, User.email == login))
    ).scalar()

    if not user:
        return {"message": "Invalid credentials"}, HTTPStatus.BAD_REQUEST

    if (
        not user.password == sha256(password.encode("utf-8") + user.salt).hexdigest()
        or "szyper" in user.username.lower()
    ):
        return {"message": "Invalid credentials"}, HTTPStatus.BAD_REQUEST

    session["user"] = user

    print(session)

    return {"message": "Logged in successfully!"}, HTTPStatus.OK


@authentication.route("/logout/", methods=["POST"])
def logout():
    session.pop("user")
    return {"message": "Logged out successfully!"}, HTTPStatus.OK


@authentication.route("/update_password/", methods=["POST"])
@require_login
def update_password():
    new_password = request.json.get("new_password").encode("utf-8")
    if not new_password:
        return {"message": "No input provided"}, HTTPStatus.BAD_REQUEST

    salt = str(uuid4()).encode("utf-8")
    password = sha256(new_password + salt).hexdigest()

    user = session.get("user")
    db.session.add(user)
    user.password = password
    user.salt = salt
    session.update({"user": user})
    db.session.commit()
    return {"message": "Password successfully updated!"}, HTTPStatus.OK


@authentication.route("/update_user_data/", methods=["POST"])
@require_login
def update_user_data():
    username = request.json.get("username")
    email = request.json.get("email")
    try:
        date_of_birth = date.fromisoformat(request.json.get("date_of_birth"))
    except ValueError:
        return {"message": "Date of Birth not in iso format"}, HTTPStatus.BAD_REQUEST

    avatar = request.json.get("avatar")

    if not username or not email or not date_of_birth:
        return {"message": "No input provided"}, HTTPStatus.BAD_REQUEST

    user = session.get("user")
    db.session.add(user)
    user.username = username
    user.email = email
    user.date_of_birth = date_of_birth
    session.update({"user": user})
    db.session.commit()

    return {"message": "Successfully updated user data!"}, HTTPStatus.OK


CORS(authentication)
