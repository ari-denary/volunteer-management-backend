"""SQLAlchemy models for User"""

from models.models import db
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import PhoneNumber

bcrypt = Bcrypt()

class User(db.Model):
    """User in the system"""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    badge_num = db.Column(
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

    _phone_number = db.Column(db.Unicode(255))
    phone_country_code = db.Column(db.Unicode(8))

    phone_number = db.composite(
        PhoneNumber,
        _phone_number,
        phone_country_code
    )

    status = db.Column(
        db.String(50),
        nullable=False,
        default="Applied"
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.now()
    )

    @classmethod
    def signup(
        cls,
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
        phone_number
    ):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
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
            phone_number=phone_number
        )

        db.session.add(user)
        return user

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
