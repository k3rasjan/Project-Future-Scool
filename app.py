from flask import Flask
from database import db
import database.models as models
from os import path

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + path.abspath(
    "database/project_future_school.sqlite"
)


db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/", methods=["GET"])
def hello_world():  # put application's code here
    result = db.session.execute(db.select(models.User))
    return result


if __name__ == "__main__":
    app.run()
