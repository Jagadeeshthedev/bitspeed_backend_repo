from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
dbname = ""
user = ""
password = ""
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@localhost/{dbname}'
db = SQLAlchemy()


def create_app():
    # creating flask web app
    db.init_app(app)
    return app

