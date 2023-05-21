# from app import app
from models.models import db
from models.User import User
# from models.Experience import Experience
from datetime import datetime
# from dateutil import relativedelta


db.drop_all()
db.create_all()

u1 = User.signup(
    badge_number=1,
    email='admin@mail.com',
    password='password',
    first_name="first",
    last_name="user",
    dob=datetime(year=2000, month=1, day=1),
    gender="Prefer not to say",
    address="123 Cherry lane",
    city="New York",
    state="NY",
    zip_code="11001",
    phone_number="9991234567",
    is_student=True,
    is_multilingual=False
)

# add users to db
db.session.add_all([u1])

db.session.commit()