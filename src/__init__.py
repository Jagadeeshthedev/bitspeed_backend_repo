import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# dbname = os.environ.get('dbname')
# user = os.environ.get('user')
# password = os.environ.get('password')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///db.sqlite3'
db = SQLAlchemy()


def create_app():
    # creating flask web app
    db.init_app(app)
    return app

