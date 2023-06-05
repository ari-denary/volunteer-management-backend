"""SQLAlchemy models for an Experience"""

from models.models import db
from models.User import User
from datetime import datetime

class Experience(db.Model):
    """A volunteer experience."""

    __tablename__ = 'experiences'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    date = db.Column(
        db.String(),
        nullable=False,
    )

    sign_in_time = db.Column(
        db.String(),
        nullable=False,
    )

    sign_out_time = db.Column(
        db.String(),
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

    def serialize(self):
        """Serialize experience data"""

        return {
            "id": self.id,
            "date": self.date,
            "sign_in_time": self.sign_in_time,
            "sign_out_time": self.sign_out_time,
            "department": self.department,
            "user_id": self.user_id
        }

    def get_duration(self):
        """Get duration of experience in hours"""

        print("sign in type is", type(self.sign_in_time))
        sign_in = datetime.fromisoformat(self.sign_in_time)
        sign_out = datetime.fromisoformat(self.sign_out_time)
        duration = sign_out - sign_in
        hours = round(duration.total_seconds()//60/60, 2)

        return hours



