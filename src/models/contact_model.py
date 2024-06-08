from datetime import datetime

import pytz

from helper_utils import get_current_time_stamp
from src import db


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phoneNumber = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    linkedId = db.Column(db.Integer, nullable=True)
    linkPrecedence = db.Column(db.String(10), nullable=False)
    createdAt = db.Column(db.DateTime, default=lambda: datetime.now(pytz.utc))
    updatedAt = db.Column(db.DateTime, default=lambda: datetime.now(pytz.utc))
    deletedAt = db.Column(db.DateTime, nullable=True)
