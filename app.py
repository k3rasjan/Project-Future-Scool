from flask import Flask, Response, jsonify, render_template
from database import db
from os import path
from routes import authentication, lesson_creation, fetching_data
from secrets import token_urlsafe
from flask_session import Session as ServerSideSession
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + path.abspath(
    "database/project_future_school.sqlite"
)


db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(authentication)
app.register_blueprint(lesson_creation)
app.register_blueprint(fetching_data)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = token_urlsafe(16)

ServerSideSession(app)
CORS(app)


@app.route("/", methods=["GET"])
def hello_world():  # put application's code here
    return "Hello World!!!"


if __name__ == "__main__":
    app.run()
