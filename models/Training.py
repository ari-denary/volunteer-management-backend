"""SQLAlchemy models for a Training"""

from models.models import db
from flask_sqlalchemy import SQLAlchemy
from models.User import User

class Training(db.Model):
    """A training"""

    __tablename__ = 'trainings'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    date = db.Column(
        db.DateTime,
        nullable=False,
    )

    name = db.Column(
        db.String(50),
        nullable=False,
    )

    description = db.Column(
        db.String,
        nullable=False,
    )

    department = db.Column(
        db.String,
        nullable=False,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey(User.id),
        nullable=False,
    )