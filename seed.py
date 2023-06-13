from app import app
from models.models import db
from models.User import User
from models.Experience import Experience
from datetime import datetime
# from dateutil import relativedelta


db.create_all()
Experience.__table__.drop(db.engine)
db.drop_all()
db.create_all()

u1 = User.signup(
    badge_number=100,
    email='u1@mail.com',
    password='password',
    first_name="u1",
    last_name="user",
    dob=(datetime(year=2000, month=1, day=1).isoformat()),
    gender="Prefer not to say",
    address="123 Cherry lane",
    city="New York",
    state="NY",
    zip_code="11001",
    phone_number="9991234567",
    is_student=True,
    is_multilingual=False
)

u2 = User.signup(
    badge_number=200,
    email='u2@mail.com',
    password='password',
    first_name="u2",
    last_name="test",
    dob=(datetime(year=2000, month=1, day=1).isoformat()),
    gender="Prefer not to say",
    address="1 Cherry lane",
    city="New York",
    state="NY",
    zip_code="11001",
    phone_number="9991234567",
    is_student=False,
    is_multilingual=False
)

admin = User.signup(
    badge_number=300,
    email='admin@mail.com',
    password='password',
    first_name="Admin",
    last_name="test",
    dob=(datetime(year=2000, month=1, day=1).isoformat()),
    gender="Prefer not to say",
    address="123 Cherry lane",
    city="New York",
    state="NY",
    zip_code="11001",
    phone_number="9991234567",
    is_student=False,
    is_multilingual=False
)

db.session.commit()

e1_sign_in = datetime(year=2022, month=1, day=5, hour=8).isoformat()

e1 = Experience(
    date=datetime(year=2022, month=1, day=5),
    sign_in_time=(datetime(year=2022, month=1, day=5, hour=8).isoformat()),
    sign_out_time=(datetime(year=2022, month=1, day=5, hour=10).isoformat()),
    department="Lab",
    user_id=1
)

e2 = Experience(
    date=datetime(year=2022, month=1, day=8),
    sign_in_time=(datetime(year=2022, month=1, day=5, hour=12).isoformat()),
    sign_out_time=(datetime(year=2022, month=1, day=5, hour=16).isoformat()),
    department="Pharmacy",
    user_id=1
)

# add experiences to db
db.session.add_all([e1, e2])

admin.is_admin = True

db.session.commit()