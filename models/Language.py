"""SQLAlchemy models for an Additional Language"""

from models.models import db
from models.User import User
from datetime import datetime

class Language(db.Model):
    """An additional language spoken by volunteer."""

    __tablename__ = 'languages'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    language = db.Column(
        db.String(),
        nullable=False,
    )
    
    fluency = db.Column(
        db.String(),
        nullable=False,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey(User.id),
        nullable=False,
    )

    def serialize(self):
        """Serialize experience data"""

        return {
            "id": self.id,
            "fluency": self.fluency,
            "language": self.language,
            "user_id": self.user_id
        }


