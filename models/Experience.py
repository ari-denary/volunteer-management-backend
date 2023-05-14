"""SQLAlchemy models for an Experience"""

from models.models import db
from flask_sqlalchemy import SQLAlchemy
from models.User import User

class Experience(db.Model):
    """A volunteer experience."""

    __tablename__ = 'experiences'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    date = db.Column(
        db.DateTime,
        nullable=False,
    )

    sign_in_time = db.Column(
        db.DateTime,
        nullable=False,
    )

    sign_out_time = db.Column(
        db.DateTime,
        nullable=False,
    )

    department = db.Column(
        db.String(50),
        nullable=False,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey(User.id),
        nullable=False,
    )
