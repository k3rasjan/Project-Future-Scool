from flask import Flask, Response, jsonify, render_template
from database import db
import database.models as models
from os import path
from routes import authentication, lesson_creation
from secrets import token_urlsafe
from flask_session import Session as ServerSideSession

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + path.abspath(
    "database/project_future_school.sqlite"
)


db.init_app(app)

with app.app_context():
    db.create_all()


class myResponse(Response):
    def __init__(self, response, **kwargs):
        self.default_mimetype = "application/json"
        super().__init__(response, **kwargs)

    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, dict):
            rv = jsonify(rv)
        return super(myResponse, cls).force_type(rv, environ)


app.response_class = myResponse

app.register_blueprint(authentication)
app.register_blueprint(lesson_creation)


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = token_urlsafe(16)

ServerSideSession(app)


@app.route("/", methods=["GET"])
def hello_world():  # put application's code here
    return "Hello World!!!"


if __name__ == "__main__":
    app.run()
