"""SQLAlchemy models for User"""

from models.models import db
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import PhoneNumber

bcrypt = Bcrypt()

class User(db.Model):
    """User in the system"""

    __tablename__ = 'users'

    def __repr__(self):
        return '<User %r %r %r>' % self.id, self.first_name, self.last_name

    # Relationships:
    #   - One User to Many Experience(s)
    #   - One User to Many Training(s)

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    badge_number = db.Column(
        db.Integer,
        unique=True,
        nullable=False,
        autoincrement=True,
    )

    email = db.Column(
        db.String(100),
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    status = db.Column(
        db.String(50),
        nullable=False,
        default="new"
    )

    first_name = db.Column(
        db.String(50),
        nullable=False,
    )

    last_name = db.Column(
        db.String(50),
        nullable=False,
    )

    dob = db.Column(
        db.DateTime,
        nullable=False,
    )

    gender = db.Column(
        db.String(50),
        nullable=False,
    )

    address = db.Column(
        db.String(50),
        nullable=False,
    )

    city = db.Column(
        db.String(50),
        nullable=False,
    )

    state = db.Column(
        db.String(50),
        nullable=False,
    )

    zip_code = db.Column(
        db.String(10),
        nullable=False,
    )

    phone_number = db.Column(
        db.String(11),
        nullable=False
    )

    is_student = db.Column(
        db.Boolean,
        nullable=False
    )

    is_multilingual = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.now()
    )

    @classmethod
    def authenticate(cls, email, password):
        """Find user with `email` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If this can't find matching user (or if password is wrong), returns
        False.
        """

        user = cls.query.filter_by(email=email).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


    @classmethod
    def signup(
        cls,
        badge_number,
        email,
        password,
        first_name,
        last_name,
        dob,
        gender,
        address,
        city,
        state,
        zip_code,
        phone_number,
        is_student,
        is_multilingual
    ):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            badge_number=badge_number,
            email=email,
            password=hashed_pwd,
            first_name=first_name,
            last_name=last_name,
            dob=dob,
            gender=gender,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            phone_number=phone_number,
            is_student=is_student,
            is_multilingual=is_multilingual
        )

        db.session.add(user)
        return user