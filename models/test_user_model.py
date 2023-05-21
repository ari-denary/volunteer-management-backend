"""User model tests."""

import os
from sqlalchemy.exc import IntegrityError
from unittest import TestCase
from flask_bcrypt import Bcrypt
from datetime import datetime

from models.models import db
from models.User import User

# To use a different database for tests, reset env variable.
# Must be before app is imported
os.environ['DATABASE_URL'] = "postgresql:///volunteer_management_test"

from app import app

bcrypt = Bcrypt()

# Create tables once for all tests.
# Data deleted & fresh test data set within each test
db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    def setUp(self):
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
            dob=datetime(year=2000, month=1, day=1),
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

    # #################### Signup Tests

    def test_valid_signup(self):
        u2 = User.signup(
            badge_number=2,
            email='u2@mail.com',
            password="password",
            first_name="u2",
            last_name="test",
            dob=datetime(year=2000, month=1, day=1),
            gender="Prefer not to say",
            address="2 Cherry lane",
            city="New York",
            state="NY",
            zip_code="11001",
            phone_number="9991234567",
            is_student=False,
            is_multilingual=False
        )

        self.assertEqual(u2.email, "u2@mail.com")
        self.assertNotEqual(u2.password, "password")
        # Bcrypt strings should start with $2b$
        self.assertTrue(u2.password.startswith("$2b$"))

    def test_invalid_signup_dupe_email(self):
        with self.assertRaises(IntegrityError):
            User.signup(
                badge_number=5,
                email='u1@mail.com',
                password="password",
                first_name="Duplicate",
                last_name="emailuser",
                dob=datetime(year=2000, month=1, day=1),
                gender="Prefer not to say",
                address="1 Cherry lane",
                city="New York",
                state="NY",
                zip_code="11001",
                phone_number="9991234567",
                is_student=True,
                is_multilingual=False
            )
            db.session.commit()

    def test_invalid_signup_dupe_badge_num(self):
        with self.assertRaises(IntegrityError):
            User.signup(
                badge_number=1,
                email='dupebadge@mail.com',
                password="password",
                first_name="Duplicate",
                last_name="badgeuser",
                dob=datetime(year=2000, month=1, day=1),
                gender="Prefer not to say",
                address="1 Cherry lane",
                city="New York",
                state="NY",
                zip_code="11001",
                phone_number="9991234567",
                is_student=True,
                is_multilingual=False
            )
            db.session.commit()

    # #################### Authentication Tests

    def test_valid_authentication(self):
        u1 = User.query.get(self.u1_id)

        u = User.authenticate("u1@mail.com", "password")
        self.assertEqual(u, u1)

    def test_invalid_email(self):
        self.assertFalse(User.authenticate("bad@mail.com", "password"))

    def test_wrong_password(self):
        self.assertFalse(User.authenticate("u1@mail.com", "bad-password"))
