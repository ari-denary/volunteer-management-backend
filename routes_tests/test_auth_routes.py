"""Auth Routes tests."""

import os
from unittest import TestCase
from datetime import datetime
from models.User import User
from models.Experience import Experience
from models.models import db

# To use a different database for tests, set env variable.
# Must be before app is imported
os.environ['DATABASE_URI'] = "postgresql:///volunteer_management_test"

from index import app

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Disable WTForms from using CSRF at all
app.config['WTF_CSRF_ENABLED'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# Create tables once for all tests.
# Data deleted & fresh test data set within each test
db.create_all()
Experience.__table__.drop(db.engine)
db.drop_all()
db.create_all()


class AuthViewTestCase(TestCase):
    def setUp(self):
        User.query.delete()

        u1 = User.signup(
            badge_number=1,
            email='u1@mail.com',
            password='password',
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

        db.session.flush()
        db.session.commit()

        self.u1_id = u1.id

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_signup_success(self):
        with self.client as c:
            resp = c.post(
                "/auth/signup",
                json={
                    "badge_number":"2",
                    "email":"u2@mail.com",
                    "password":"password",
                    "first_name":"u2",
                    "last_name":"test",
                    "dob":"2000-01-01 00:00:00",
                    "gender":"Prefer not to say",
                    "address":"2 Cherry lane",
                    "city":"New York",
                    "state":"NY",
                    "zip_code":"11001",
                    "phone_number":"9991234567",
                    "is_student":True,
                    "is_multilingual":False
                })

            self.assertIsInstance(resp.json["token"], str)

    def test_signup_dupe_email(self):
        with self.client as c:
            resp = c.post(
                "/auth/signup",
                json={
                    "badge_number":"3",
                    "email":"u1@mail.com",
                    "password":"password",
                    "first_name":"duplicate email",
                    "last_name":"test",
                    "dob":"2000-01-01 00:00:00",
                    "gender":"Prefer not to say",
                    "address":"1 Cherry lane",
                    "city":"New York",
                    "state":"NY",
                    "zip_code":"11001",
                    "phone_number":"9991234567",
                    "is_student": True,
                    "is_multilingual": False
                })

            self.assertEqual(
                resp.json["errors"],
                "Invalid data: email or badge number already in use"
            )

    def test_signup_dupe_badge_num(self):
        with self.client as c:
            resp = c.post(
                "/auth/signup",
                json={
                    "badge_number":"1",
                    "email":"u3@mail.com",
                    "password":"password",
                    "first_name":"duplicate badge",
                    "last_name":"test",
                    "dob":"2000-01-01 00:00:00",
                    "gender":"Prefer not to say",
                    "address":"1 Cherry lane",
                    "city":"New York",
                    "state":"NY",
                    "zip_code":"11001",
                    "phone_number":"9991234567",
                    "is_student": True,
                    "is_multilingual": False
                })

            self.assertEqual(
                resp.json["errors"],
                "Invalid data: email or badge number already in use"
            )

    def test_login(self):
        with self.client as c:
            resp = c.post(
                "/auth/login",
                json={
                    "email": "u1@mail.com",
                    "password": "password",
                })

            self.assertIsInstance(resp.json["token"], str)

    def test_login_wrong_password(self):
        with self.client as c:
            resp = c.post(
                "/auth/login",
                json={
                    "email": "u1@mail.com",
                    "password": "badpassword",
                })

            self.assertEqual(resp.json["errors"], "Invalid credentials")

    def test_login_wrong_password_email(self):
        with self.client as c:
            resp = c.post(
                "/auth/login",
                json={
                    "email": "bad@email.com",
                    "password": "badpassword",
                })

            self.assertEqual(resp.json["errors"], "Invalid credentials")