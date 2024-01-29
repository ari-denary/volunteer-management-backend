"""SQLAlchemy models for User"""

from models.models import db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class User(db.Model):
    """User in the system"""

    __tablename__ = 'users'

    # def __repr__(self):
    #     return ('<User %r %r %r>' % self.id, self.first_name, self.last_name)

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
    
    school_email = db.Column(
        db.String(100),
        nullable=True,
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
        db.String(100),
        nullable=False,
    )

    last_name = db.Column(
        db.String(100),
        nullable=False,
    )

    dob = db.Column(
        db.String(),
        nullable=False,
    )

    gender = db.Column(
        db.String(100),
        nullable=False,
    )
    
    pronouns = db.Column(
        db.String(100),
        nullable=True
    )
    
    race = db.Column(
        db.String(100),
        nullable=True
    )
    
    ethnicity = db.Column(
        db.String(100),
        nullable=True
    )

    address = db.Column(
        db.String(100),
        nullable=False,
    )

    city = db.Column(
        db.String(100),
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
    
    phone_carrier = db.Column(
        db.String(100),
        nullable=True
    )

    is_student = db.Column(
        db.Boolean,
        nullable=False
    )
    
    type_of_student = db.Column(
        db.String(100),
        nullable=True
    )
    
    school = db.Column(
        db.String(100),
        nullable=True
    )
    
    degree = db.Column(
        db.String(100),
        nullable=True
    )
    
    anticipated_graduation = db.Column(
        db.String(100),
        nullable=True
    )
    
    major = db.Column(
        db.String(100),
        nullable=True
    )
    
    minor = db.Column(
        db.String(100),
        nullable=True
    )
    
    classification = db.Column(
        db.String(100),
        nullable=True
    )
    
    is_healthcare_provider = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )
    
    type_of_provider = db.Column(
        db.String(100),
        nullable=True
    )
    
    employer = db.Column(
        db.String(100),
        nullable=True
    )

    is_multilingual = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )
    
    is_admin = db.Column(
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
        is_healthcare_provider,
        is_multilingual,
        badge_number=None,
        status=None,
        pronouns=None,
        race=None,
        ethnicity=None,
        phone_carrier=None,
        type_of_student=None,
        school=None,
        anticipated_graduation=None,
        major=None,
        minor=None,
        classification=None,
        degree=None,
        school_email=None,
        type_of_provider=None,
        employer=None,
    ):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            status=status,
            badge_number=badge_number,
            email=email,
            password=hashed_pwd,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            dob=dob,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            phone_number=phone_number,
            is_student=is_student,
            is_healthcare_provider=is_healthcare_provider,
            is_multilingual=is_multilingual,
            school_email=school_email,
            pronouns=pronouns,
            race=race,
            ethnicity=ethnicity,
            phone_carrier=phone_carrier,
            type_of_student=type_of_student,
            school=school,
            anticipated_graduation=anticipated_graduation,
            major=major,
            minor=minor,
            classification=classification,
            degree=degree,
            type_of_provider=type_of_provider,
            employer=employer,
        )

        db.session.add(user)
        return user

    def serialize(self):
        """Serialize user data"""

        return {
            "id": self.id,
            "badge_number": self.badge_number,
            "email": self.email,
            "school_email": self.school_email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "dob": self.dob,
            "gender": self.gender,
            "pronouns": self.pronouns,
            "race": self.race,
            "ethnicity": self.ethnicity,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "zip_code": self.zip_code,
            "phone_number": self.phone_number,
            "phone_carrier": self.phone_carrier,
            "is_student": self.is_student,
            "type_of_student": self.type_of_student,
            "school": self.school,
            "anticipated_graduation": self.anticipated_graduation,
            "major": self.major,
            "minor": self.minor,
            "classification": self.classification,
            "degree": self.degree,
            "is_healthcare_provider": self.is_healthcare_provider,
            "type_of_provider": self.type_of_provider,
            "employer": self.employer,
            "is_multilingual": self.is_multilingual,
            "is_admin": self.is_admin,
            "status": self.status,
            "created_at": self.created_at
        }