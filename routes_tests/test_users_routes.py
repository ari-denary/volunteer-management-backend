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

BAD_TOKEN = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NDk3" +
    "OTk5OSwianRpIjoiNGI2NWQ3MTYtNTRkOS00NmFiLTg4YTQtZjdlNzY5YTk4OTVlIiwidHlw" +
    "ZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjg0OTc5OTk5LCJleHAiOjE2ODQ5ODA4OTl9" +
    "TEfMrC8bzoxsfBU4M1Vabw"
)


class UsersViewsTestCase(TestCase):
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
        admin.status = "active"
        u1.status = "active"
        db.session.add_all([e1, e2])
        db.session.commit()

        self.u1_id = u1.id
        self.u2_id = u2.id
        self.admin_id = admin.id

        self.client = app.test_client()

        with self.client as c:
            resp1 = c.post(
                "/auth/login",
                json={
                    "email": "u1@mail.com",
                    "password": "password",
                })

            self.u1_token = resp1.json["token"]

            resp2 = c.post(
                "/auth/login",
                json={
                    "email": "u2@mail.com",
                    "password": "password",
                })

            self.u2_token = resp2.json["token"]

            resp_admin = c.post(
                "/auth/login",
                json={
                    "email": "admin@mail.com",
                    "password": "password",
                })

            self.admin_token = resp_admin.json["token"]

    def tearDown(self):
        db.session.rollback()

########################################################################
# GET /users tests

    def test_get_users_success_admin(self):
        """Admin can successfully get list of all users"""

        with self.client as c:
            self.maxDiff = None
            resp = c.get(
                f"/users",
                headers={"AUTHORIZATION": f"Bearer {self.admin_token}"}
            )

            users = [u for u in resp.json['users']]
            for u in users:
                del u['id']

            self.assertEqual(len(users), 3)
            self.assertIn(
                {
                    "badge_number": 1,
                    "email": "u1@mail.com",
                    "first_name": "u1",
                    "is_admin": False,
                    "is_multilingual": False,
                    "is_student": True,
                    "last_name": "test",
                    "status": "active",
                    "experience_hours": 10
                },
                users
            )
            self.assertIn(
                {
                    "badge_number": 2,
                    "email": "u2@mail.com",
                    "first_name": "u2",
                    "is_admin": False,
                    "is_multilingual": False,
                    "is_student": False,
                    "last_name": "test",
                    "status": "new",
                    "experience_hours": 0
                },
                users
            )
            self.assertIn(
                {
                    "badge_number": 3,
                    "email": 'admin@mail.com',
                    "first_name": "Admin",
                    "is_admin": True,
                    "is_multilingual": False,
                    "is_student": False,
                    "last_name": "test",
                    "status": "active",
                    "experience_hours": 0
                },
                users
            )
            self.assertListEqual(
                users,
                [
                    {
                        "badge_number": 1,
                        "email": "u1@mail.com",
                        "experience_hours": 10,
                        "first_name": "u1",
                        "is_admin": False,
                        "is_multilingual": False,
                        "is_student": True,
                        "last_name": "test",
                        "status": "active"
                    },
                    {
                        "badge_number": 3,
                        "email": 'admin@mail.com',
                        "experience_hours": 0,
                        "first_name": "Admin",
                        "is_admin": True,
                        "is_multilingual": False,
                        "is_student": False,
                        "last_name": "test",
                        "status": "active"
                    },
                    {
                        "badge_number": 2,
                        "email": "u2@mail.com",
                        "experience_hours": 10,
                        "first_name": "u2",
                        "is_admin": False,
                        "is_multilingual": False,
                        "is_student": False,
                        "last_name": "test",
                        "status": "new"
                    }
                ]
            )

    def test_get_users_fail_non_admin(self):
        """Non-admin user can NOT get list of all users"""

        with self.client as c:
            resp = c.get(
                f"/users",
                headers={"AUTHORIZATION": f"Bearer {self.u1_token}"}
            )

            self.assertEqual(resp.status_code, 401)
            self.assertEqual(resp.json['errors'], "Unauthorized")

    def test_get_users_fail_no_token(self):
        """Can NOT get list of all users without token"""

        with self.client as c:
            resp = c.get(f"/users")

            self.assertEqual(resp.status_code, 401)
            self.assertIn("Missing JWT", resp.json['msg'])

    def test_get_users_fail_invalid_token(self):
        """Can NOT get list of all users with invalid token"""

        with self.client as c:
            resp = c.get(
                f"/users",
                headers={"AUTHORIZATION": f"Bearer {BAD_TOKEN}"}
            )

            self.assertEqual(resp.status_code, 401)
            self.assertEqual(resp.json['errors'], "Invalid token")


########################################################################
# GET /users/<id> tests

    def test_get_user_success_same_user(self):
        """User can successfully get their own details"""

        with self.client as c:
            resp = c.get(
                f"/users/{self.u1_id}",
                headers={"AUTHORIZATION": f"Bearer {self.u1_token}"}
            )

            user = resp.json['user']
            self.assertEqual(user['email'], "u1@mail.com")
            self.assertEqual(user['id'], self.u1_id)

    def test_get_user_success_admin(self):
        """Admin can successfully get a user's details"""

        with self.client as c:
            resp = c.get(
                f"/users/{self.u1_id}",
                headers={"AUTHORIZATION": f"Bearer {self.admin_token}"}
            )

            user = resp.json['user']
            self.assertEqual(user['email'], "u1@mail.com")
            self.assertEqual(user['id'], self.u1_id)

    def test_get_user_fail_diff_user(self):
        """User can NOT get another user's details"""

        with self.client as c:
            resp = c.get(
                f"/users/{self.u1_id}",
                headers={"AUTHORIZATION": f"Bearer {self.u2_token}"}
            )

            self.assertEqual(resp.status_code, 401)
            self.assertEqual(resp.json['errors'], "Unauthorized")

    def test_get_user_fail_no_token(self):
        """Can NOT get a user without a token"""

        with self.client as c:
            resp = c.get(f"/users/{self.u1_id}")

            self.assertEqual(resp.status_code, 401)
            self.assertIn("Missing JWT", resp.json['msg'])

    def test_get_user_fail_invalid_token(self):
        """Can NOT get a user with invalid token"""

        with self.client as c:
            resp = c.get(
                f"/users/{self.u1_id}",
                headers={"AUTHORIZATION": f"Bearer {BAD_TOKEN}"}
            )

            self.assertEqual(resp.status_code, 401)
            self.assertEqual(resp.json['errors'], "Invalid token")

########################################################################
# GET /users/<id>/experiences tests

    def test_get_user_experiences_success_all_same_user(self):
        """User can successfully get a list of their own experiences"""

        with self.client as c:
            resp1 = c.get(
                f"/users/{self.u1_id}/experiences",
                headers={"AUTHORIZATION": f"Bearer {self.u1_token}"}
            )

            resp2 = c.get(
                f"/users/{self.u2_id}/experiences",
                headers={"AUTHORIZATION": f"Bearer {self.u2_token}"}
            )

            self.assertEqual(len(resp1.json['user_experiences']), 2)
            self.assertEqual(len(resp2.json['user_experiences']), 0)

    # get_user_experiences_success_open_same_user

    def test_get_user_experiences_success_all_admin(self):
        """Admin can successfully get list of a user's experiences"""

        with self.client as c:
            resp1 = c.get(
                f"/users/{self.u1_id}/experiences",
                headers={"AUTHORIZATION": f"Bearer {self.admin_token}"}
            )

            resp2 = c.get(
                f"/users/{self.u2_id}/experiences",
                headers={"AUTHORIZATION": f"Bearer {self.admin_token}"}
            )

            self.assertEqual(len(resp1.json['user_experiences']), 2)
            self.assertEqual(len(resp2.json['user_experiences']), 0)

    # get_user_experiences_success_open_admin

    def test_get_user_experiences_fail_all_diff_user(self):
        """User can NOT get a list of another users' experiences"""

        with self.client as c:
            resp = c.get(
                    f"/users/{self.u2_id}/experiences",
                    headers={"AUTHORIZATION": f"Bearer {self.u1_token}"}
                )

            self.assertEqual(resp.status_code, 401)
            self.assertEqual(resp.json['errors'], "Unauthorized")

    # get_user_experiences_fail_open_diff_user

    def test_get_user_experiences_fail_no_token(self):
        """Can NOT get a list of a users' experiences without token"""

        with self.client as c:
            resp = c.get(f"/users/{self.u2_id}/experiences")

            self.assertEqual(resp.status_code, 401)
            self.assertIn("Missing JWT", resp.json['msg'])

    # get_user_experiences_fail_open_no_token

    def test_get_user_experiences_fail_invalid_token(self):
        """Can NOT get a list of a users' experiences with invalid token"""

        with self.client as c:
            resp = c.get(
                    f"/users/{self.u2_id}/experiences",
                    headers={"AUTHORIZATION": f"Bearer {BAD_TOKEN}"}
                )

            self.assertEqual(resp.status_code, 401)
            self.assertEqual(resp.json['errors'], "Invalid token")

    # get_user_experiences_fail_open_invalid_token

########################################################################
# POST /users/<id>/experiences tests

# success create new experience same user

# success create new experience admin

# fail create new experience not all required inputs sent

# fail create new experience diff user

# fail create new experience no token

# fail create new experience invalid token


########################################################################
# PATCH /users/<id>/experiences tests

# success update experience same user

# success update experience admin

# update experience does not update other data (besides sign out/dept) same user

# update experience does not update other data (besides sign out/dept) admin

# fail update experience missing sign out time same user

# fail update experience missing sign out time admin

# fail update experience diff user

# fail update experience no token

# fail update experience invalid token