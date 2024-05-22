from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/dbname'
db = SQLAlchemy()


def create_app():
    # not using sqlalchemy event system, hence disabling it

    # Set up extensions
    # mail.init_app(app)
    db.init_app(app)
    return app

