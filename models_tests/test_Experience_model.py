"""Experience model tests."""

import os
from unittest import TestCase
from flask_bcrypt import Bcrypt
from datetime import datetime

from models.models import db
from models.User import User
from models.Experience import Experience

# To use a different database for tests, set env variable.
# Must be before app is imported
os.environ['DATABASE_URI'] = "postgresql:///volunteer_management_test"

from app import app

bcrypt = Bcrypt()

# Create tables once for all tests.
# Data deleted & fresh test data set within each test
db.create_all()
Experience.__table__.drop(db.engine)
db.drop_all()
db.create_all()


class ExperienceModelTestCase(TestCase):
    def setUp(self):
        Experience.query.delete()
        User.query.delete()

        hashed_password = (bcrypt
            .generate_password_hash("password")
            .decode('UTF-8')
        )

        u1 = User(
            badge_number=1,
            email='u1@mail.com',
            password=hashed_password,
            first_name="u1",
            last_name="test",
            dob=datetime(year=2000, month=1, day=1).isoformat(),
            gender="Prefer not to say",
            address="1 Cherry lane",
            city="New York",
            state="NY",
            zip_code="11001",
            phone_number="9991234567",
            is_student=True,
            is_multilingual=False
        )

        db.session.add(u1)
        db.session.commit()

        self.u1_id = u1.id

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

############################################################
# get_duration Tests

    # def test_get_duration(self):
# TODO: Add test for get_duration