"""User Routes tests."""

import os
from unittest import TestCase
from datetime import datetime
from models.User import User
from models.Experience import Experience
from models.models import db

# To use a different database for tests, reset env variable.
# Must be before app is imported
os.environ['DATABASE_URI'] = "postgresql:///volunteer_management_test"

from app import app

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
        Experience.query.delete()
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

        u2 = User.signup(
            badge_number=2,
            email='u2@mail.com',
            password='password',
            first_name="u2",
            last_name="test",
            dob=datetime(year=2000, month=1, day=1),
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
            badge_number=3,
            email='admin@mail.com',
            password='password',
            first_name="Admin",
            last_name="test",
            dob=datetime(year=2000, month=1, day=1),
            gender="Prefer not to say",
            address="1 Cherry lane",
            city="New York",
            state="NY",
            zip_code="11001",
            phone_number="9991234567",
            is_student=False,
            is_multilingual=False
        )

        db.session.flush()
        db.session.commit()

        e1 = Experience(
            date=datetime(year=2022, month=1, day=5),
            sign_in_time=datetime(year=2022, month=1, day=5, hour=8),
            sign_out_time=datetime(year=2022, month=1, day=5, hour=10),
            department="Lab",
            user_id=u1.id
        )

        e2 = Experience(
            date=datetime(year=2022, month=1, day=8),
            sign_in_time=datetime(year=2022, month=1, day=5, hour=12),
            sign_out_time=datetime(year=2022, month=1, day=5, hour=16),
            department="Pharmacy",
            user_id=u1.id
        )

        admin.is_admin = True
        db.session.add_all([e1, e2])
        db.session.commit()

        self.u1_id = u1.id
        self.u2_id = u2.id
        self.admin_id = admin.id

        self.client = app.test_client()

        with self.client as c:
            resp1 = c.post(
                "/login",
                json={
                    "email": "u1@mail.com",
                    "password": "password",
                })

            self.u1_token = resp1.json["token"]

            resp2 = c.post(
                "/login",
                json={
                    "email": "u2@mail.com",
                    "password": "password",
                })

            self.u2_token = resp2.json["token"]

            resp_admin = c.post(
                "/login",
                json={
                    "email": "admin@mail.com",
                    "password": "password",
                })

            self.admin_token = resp_admin.json["token"]

    def tearDown(self):
        db.session.rollback()

    def test_get_user_success_same_user(self):
        with self.client as c:
            resp = c.get(f"/users/{self.u1_id}", headers={
                "AUTHORIZATION": f"Bearer {self.u1_token}"
            })

            user = resp.json['user']
            self.assertEqual(user['email'], "u1@mail.com")
            self.assertEqual(user['id'], self.u1_id)

    def test_get_user_success_admin(self):
        with self.client as c:
            resp = c.get(f"/users/{self.u1_id}", headers={
                "AUTHORIZATION": f"Bearer {self.admin_token}"
            })

            user = resp.json['user']
            self.assertEqual(user['email'], "u1@mail.com")
            self.assertEqual(user['id'], self.u1_id)

    def test_get_user_fail_diff_user(self):
        with self.client as c:
            resp = c.get(f"/users/{self.u1_id}", headers={
                "AUTHORIZATION": f"Bearer {self.u2_token}"
            })

            self.assertEqual(resp.status_code, 401)
            self.assertEqual(resp.json['errors'], "Unauthorized")

    def test_get_user_fail_no_token(self):
        with self.client as c:
            resp = c.get(f"/users/{self.u1_id}")

            self.assertEqual(resp.status_code, 401)
            self.assertIn("Missing JWT", resp.json['msg'])

    def test_get_user_fail_invalid_token(self):
        with self.client as c:
            bad_token = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9eyJmcmVzaCI6ZmFsc" +
            "2UsImlhdCI6MTY4NDk3OTk5OSwianRpIjoiNGI2NWQ3MTYtNTRkOS00NmFiLTg4YT" +
            "QtZjdlNzY5YTk4OTVlIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjg" +
            "0OTc5OTk5LCJleHAiOjE2ODQ5ODA4OTl9TEfMrC8bzoxsfBU4M1Vabw")

            resp = c.get(f"/users/{self.u1_id}", headers={
                "AUTHORIZATION": f"Bearer {bad_token}"
            })

            self.assertEqual(resp.status_code, 401)
            self.assertEqual(resp.json['errors'], "Invalid token")