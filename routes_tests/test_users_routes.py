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

EXPERIENCE_DATA_DATE_TIME = datetime(
    year=2022,
    month=1,
    day=8,
    hour=12,
    minute=12,
    second=1,
    microsecond=1
).isoformat()


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

        u2 = User.signup(
            badge_number=2,
            email='u2@mail.com',
            password='password',
            first_name="u2",
            last_name="test",
            dob=datetime(year=2000, month=1, day=1).isoformat(),
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
            dob=datetime(year=2000, month=1, day=1).isoformat(),
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
            date=datetime(year=2022, month=1, day=5).isoformat(),
            sign_in_time=datetime(year=2022, month=1, day=5, hour=8).isoformat(),
            sign_out_time=datetime(year=2022, month=1, day=5, hour=10).isoformat(),
            department="lab",
            user_id=u1.id
        )

        e2 = Experience(
            date=datetime(year=2022, month=1, day=8).isoformat(),
            sign_in_time=datetime(year=2022, month=1, day=8, hour=12).isoformat(),
            sign_out_time=datetime(year=2022, month=1, day=8, hour=16).isoformat(),
            department="pharmacy",
            user_id=u1.id
        )

        e3 = Experience(
            date=datetime(year=2022, month=1, day=10).isoformat(),
            sign_in_time=datetime(year=2022, month=1, day=10, hour=12).isoformat(),
            sign_out_time=None,
            department="pharmacy",
            user_id=u1.id
        )

        admin.is_admin = True
        admin.status = "active"
        u1.status = "active"
        db.session.add_all([e1, e2, e3])
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
                    "experience_hours": 6.0,
                    "first_name": "u1",
                    "is_admin": False,
                    "is_multilingual": False,
                    "is_student": True,
                    "last_name": "test",
                    "status": "active"
                },
                users
            )
            self.assertIn(
                {
                    "badge_number": 2,
                    "email": "u2@mail.com",
                    "experience_hours": 0,
                    "first_name": "u2",
                    "is_admin": False,
                    "is_multilingual": False,
                    "is_student": False,
                    "last_name": "test",
                    "status": "new"
                },
                users
            )
            self.assertIn(
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
                users
            )
            # self.assertListEqual(
            #     users,
            #     [
            #         {
            #             "badge_number": 1,
            #             "email": "u1@mail.com",
            #             "experience_hours": 6.0,
            #             "first_name": "u1",
            #             "is_admin": False,
            #             "is_multilingual": False,
            #             "is_student": True,
            #             "last_name": "test",
            #             "status": "active"
            #         },
            #         {
            #             "badge_number": 3,
            #             "email": 'admin@mail.com',
            #             "experience_hours": 0,
            #             "first_name": "Admin",
            #             "is_admin": True,
            #             "is_multilingual": False,
            #             "is_student": False,
            #             "last_name": "test",
            #             "status": "active"
            #         },
            #         {
            #             "badge_number": 2,
            #             "email": "u2@mail.com",
            #             "experience_hours": 0,
            #             "first_name": "u2",
            #             "is_admin": False,
            #             "is_multilingual": False,
            #             "is_student": False,
            #             "last_name": "test",
            #             "status": "new"
            #         }
            #     ]
            # )

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
# GET /users/<user_id> tests

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
# GET /users/<user_id>/experiences tests

    def test_get_all_user_experiences_success_same_user(self):
        """User can successfully get a list of their own experiences"""

        with self.client as c:
            resp = c.get(
                f"/users/{self.u1_id}/experiences",
                headers={"AUTHORIZATION": f"Bearer {self.u1_token}"}
            )

            user_experiences = [u for u in resp.json['user_experiences']]
            for e in user_experiences:
                del e['id']

            self.assertEqual(len(resp.json['user_experiences']), 3)
            self.assertIn(
                {
                    "date": "2022-01-05T00:00:00",
                    "sign_in_time": "2022-01-05T08:00:00",
                    "sign_out_time": "2022-01-05T10:00:00",
                    "department": "lab",
                    "user_id": self.u1_id
                },
                user_experiences
            )
            self.assertIn(
                {
                    "date": "2022-01-08T00:00:00",
                    "sign_in_time": "2022-01-08T12:00:00",
                    "sign_out_time": "2022-01-08T16:00:00",
                    "department": "pharmacy",
                    "user_id": self.u1_id
                },
                user_experiences
            )
            self.assertIn(
                {
                    "date": "2022-01-10T00:00:00",
                    "sign_in_time": "2022-01-10T12:00:00",
                    "sign_out_time": None,
                    "department": "pharmacy",
                    "user_id": self.u1_id
                },
                user_experiences
            )

    def test_get_all_user_experiences_success_admin(self):
        """Admin can successfully get list of a user's experiences"""

        with self.client as c:
            resp = c.get(
                f"/users/{self.u1_id}/experiences",
                headers={"AUTHORIZATION": f"Bearer {self.admin_token}"}
            )

            user_experiences = [u for u in resp.json['user_experiences']]
            for e in user_experiences:
                del e['id']

            self.assertEqual(len(resp.json['user_experiences']), 3)
            self.assertIn(
                {
                    "date": "2022-01-05T00:00:00",
                    "sign_in_time": "2022-01-05T08:00:00",
                    "sign_out_time": "2022-01-05T10:00:00",
                    "department": "lab",
                    "user_id": self.u1_id
                },
                user_experiences
            )
            self.assertIn(
                {
                    "date": "2022-01-08T00:00:00",
                    "sign_in_time": "2022-01-08T12:00:00",
                    "sign_out_time": "2022-01-08T16:00:00",
                    "department": "pharmacy",
                    "user_id": self.u1_id
                },
                user_experiences
            )
            self.assertIn(
                {
                    "date": "2022-01-10T00:00:00",
                    "sign_in_time": "2022-01-10T12:00:00",
                    "sign_out_time": None,
                    "department": "pharmacy",
                    "user_id": self.u1_id
                },
                user_experiences
            )

    def test_get_incomplete_user_experiences_success_same_user(self):
        """
        Same user can get list of their own experiences whose sign-out time is
        None
        """

        with self.client as c:
            resp = c.get(
                f"/users/{self.u1_id}/experiences?incomplete",
                headers={"AUTHORIZATION": f"Bearer {self.u1_token}"}
            )

            user_experiences = [u for u in resp.json['user_experiences']]
            for e in user_experiences:
                del e['id']

            self.assertEqual(len(resp.json['user_experiences']), 1)
            self.assertIn(
                {
                    "date": "2022-01-10T00:00:00",
                    "sign_in_time": "2022-01-10T12:00:00",
                    "sign_out_time": None,
                    "department": "pharmacy",
                    "user_id": self.u1_id
                },
                user_experiences
            )

    def test_get_incomplete_user_experiences_success_admin(self):
        """
        Admin can get list of a user's experiences whose sign-out time is
        None
        """

        with self.client as c:
            resp = c.get(
                f"/users/{self.u1_id}/experiences?incomplete",
                headers={"AUTHORIZATION": f"Bearer {self.admin_token}"}
            )

            user_experiences = [u for u in resp.json['user_experiences']]
            for e in user_experiences:
                del e['id']

            self.assertEqual(len(resp.json['user_experiences']), 1)
            self.assertIn(
                {
                    "date": "2022-01-10T00:00:00",
                    "sign_in_time": "2022-01-10T12:00:00",
                    "sign_out_time": None,
                    "department": "pharmacy",
                    "user_id": self.u1_id
                },
                user_experiences
            )

    def test_get_no_user_experiences_success_same_user(self):
        """Same user gets an empty list if they have no experiences"""

        with self.client as c:
            resp1 = c.get(
                f"/users/{self.u2_id}/experiences",
                headers={"AUTHORIZATION": f"Bearer {self.u2_token}"}
            )

            resp2 = c.get(
                f"/users/{self.u2_id}/experiences?incomplete",
                headers={"AUTHORIZATION": f"Bearer {self.u2_token}"}
            )

            self.assertEqual(len(resp1.json['user_experiences']), 0)
            self.assertEqual(len(resp2.json['user_experiences']), 0)

    def test_get_no_user_experiences_success_admin(self):
        """Admin gets an empty list if a user has no experiences"""

        with self.client as c:
            resp1 = c.get(
                f"/users/{self.u2_id}/experiences",
                headers={"AUTHORIZATION": f"Bearer {self.admin_token}"}
            )

            resp2 = c.get(
                f"/users/{self.u2_id}/experiences?incomplete",
                headers={"AUTHORIZATION": f"Bearer {self.admin_token}"}
            )

            self.assertEqual(len(resp1.json['user_experiences']), 0)
            self.assertEqual(len(resp2.json['user_experiences']), 0)

    def test_get_user_experiences_fail_diff_user(self):
        """User can NOT get a list of another users' experiences"""

        with self.client as c:
            resp1 = c.get(
                    f"/users/{self.u2_id}/experiences",
                    headers={"AUTHORIZATION": f"Bearer {self.u1_token}"}
                )

            resp2 = c.get(
                    f"/users/{self.u2_id}/experiences?incomplete",
                    headers={"AUTHORIZATION": f"Bearer {self.u1_token}"}
                )

            self.assertEqual(resp1.status_code, 401)
            self.assertEqual(resp2.status_code, 401)
            self.assertEqual(resp1.json['errors'], "Unauthorized")
            self.assertEqual(resp2.json['errors'], "Unauthorized")

    def test_get_user_experiences_fail_no_token(self):
        """Can NOT get a list of a users' experiences without token"""

        with self.client as c:
            resp1 = c.get(f"/users/{self.u2_id}/experiences")
            resp2 = c.get(f"/users/{self.u2_id}/experiences?incomplete")

            self.assertEqual(resp1.status_code, 401)
            self.assertEqual(resp2.status_code, 401)
            self.assertIn("Missing JWT", resp1.json['msg'])
            self.assertIn("Missing JWT", resp2.json['msg'])

    def test_get_user_experiences_fail_invalid_token(self):
        """Can NOT get a list of a users' experiences with invalid token"""

        with self.client as c:
            resp1 = c.get(
                    f"/users/{self.u2_id}/experiences",
                    headers={"AUTHORIZATION": f"Bearer {BAD_TOKEN}"}
                )
            resp2 = c.get(
                    f"/users/{self.u2_id}/experiences",
                    headers={"AUTHORIZATION": f"Bearer {BAD_TOKEN}"}
                )

            self.assertEqual(resp1.status_code, 401)
            self.assertEqual(resp2.status_code, 401)
            self.assertEqual(resp1.json['errors'], "Invalid token")
            self.assertEqual(resp2.json['errors'], "Invalid token")

# ########################################################################
# # POST /users/<user_id>/experiences tests

    def test_create_user_experience_success_same_user(self):
        """Same user can create a new experience for themselves"""

        experience_data = {
            "date": EXPERIENCE_DATA_DATE_TIME,
            "sign_in_time": EXPERIENCE_DATA_DATE_TIME,
            "department": "pharmacy",
            "user_id": self.u2_id
        }

        with self.client as c:
            resp = c.post(
                    f"/users/{self.u2_id}/experiences",
                    headers={"AUTHORIZATION": f"Bearer {self.u2_token}"},
                    json=experience_data
            )
            print("experience_data = ", experience_data)
            print("resp.json for success same user = ", resp.json)
            resp_json = resp.json['user_experience']
            del resp_json['id']

            experience_data = Experience.query.filter_by(user_id=self.u2_id).all()

            self.assertEqual(resp_json, {
                "date": EXPERIENCE_DATA_DATE_TIME,
                "sign_in_time": EXPERIENCE_DATA_DATE_TIME,
                "sign_out_time": None,
                "department": "pharmacy",
                "user_id": self.u2_id
            })
            self.assertEqual(len(experience_data), 1)


# # TODO: success create new experience admin
#     def test_create_user_experience_success_admin(self):
#         """Admin can create a new experience for a user"""

#         experience_data = {
#             "date": datetime(year=2022, month=1, day=8).isoformat(),
#             "sign_in_time": datetime(year=2022, month=1, day=8, hour=12).isoformat(),
#             "department": "pharmacy",
#             "user_id": self.u2_id
#         }

#         with self.client as c:
#             resp = c.post(
#                     f"/users/{self.u2_id}/experiences",
#                     headers={"AUTHORIZATION": f"Bearer {self.admin_token}"},
#                     json=experience_data
#             )

#             print("resp.json for success admin = ", resp.json)
#             resp_json = resp.json['user_experience']
#             del resp_json['id']

#             # TODO: check this:
#             experience_data = Experience.query.filter_by(user_id=self.u2_id).all()

#             self.assertEqual(resp_json, {
#                 "date": "2022-01-08T00:00:00",
#                 "sign_in_time": "2022-01-08T12:00:00",
#                 "sign_out_time": None,
#                 "department": "pharmacy",
#                 "user_id": self.u2_id
#             })
#             self.assertEqual(len(experience_data), 1)


# # TODO: fail create new experience not all required inputs sent same user
#     def test_create_user_experience_fail_incomplete_inputs_same_user(self):
#         """Same user can NOT create a new experience with incomplete inputs"""

#         incomplete_data = {
#             "date": datetime(year=2022, month=1, day=8).isoformat(),
#             "department": "pharmacy",
#             "user_id": self.u2_id
#         }

#         with self.client as c:
#             resp = c.post(
#                     f"/users/{self.u2_id}/experiences",
#                     headers={"AUTHORIZATION": f"Bearer {self.u2_token}"},
#                     json=incomplete_data
#             )

#             self.assertEqual(
#                 {'sign_in_time': ['This field is required.']},
#                 resp.json['errors']
#             )

# # TODO: fail create new experience not all required inputs sent admin
#     def test_create_user_experience_fail_incomplete_inputs_admin(self):
#         """Admin can NOT create a new experience for user with incomplete inputs"""

#         incomplete_data = {
#             "date": datetime(year=2022, month=1, day=8).isoformat(),
#             "department": "pharmacy",
#             "user_id": self.u2_id
#         }

#         with self.client as c:
#             resp = c.post(
#                     f"/users/{self.u2_id}/experiences",
#                     headers={"AUTHORIZATION": f"Bearer {self.admin_token}"},
#                     json=incomplete_data
#             )

#             self.assertEqual(
#                 {'sign_in_time': ['This field is required.']},
#                 resp.json['errors']
#             )

# # TODO: fail create new experience not all required inputs sent same user
#     def test_create_user_experience_fail_invalid_inputs_same_user(self):
#         """Same user can NOT create a new experience with invalid inputs"""

#         invalid_data = {
#             "date": "bob",
#             "sign_in_time": datetime(year=2022, month=1, day=20, hour=12).isoformat(),
#             "department": "lab",
#             "user_id": self.u2_id
#         }

#         with self.client as c:
#             resp = c.post(
#                     f"/users/{self.u2_id}/experiences",
#                     headers={"AUTHORIZATION": f"Bearer {self.u2_token}"},
#                     json=invalid_data
#             )

#             print("invalid input same user resp.json = ", resp.json)

#             self.assertEqual({
#                 'user_id': [
#                     'Not a valid integer value.',
#                     'Not a valid integer value.'
#             ]},
#                 resp.json['errors']
#             )

# # TODO: fail create new experience not all required inputs sent admin
#     def test_create_user_experience_fail_invalid_inputs_admin(self):
#         """Admin can NOT create a new experience for user with invalid inputs"""

#         invalid_data = {
#             "date": datetime(year=2022, month=1, day=20).isoformat(),
#             "sign_in_time": datetime(year=2022, month=1, day=20, hour=12).isoformat(),
#             "department": "lab",
#             "user_id": "bob"
#         }

#         with self.client as c:
#             resp = c.post(
#                     f"/users/{self.u2_id}/experiences",
#                     headers={"AUTHORIZATION": f"Bearer {self.admin_token}"},
#                     json=invalid_data
#             )

#             print("invalid input Admin resp.json = ", resp.json)

#             self.assertEqual({
#                 'user_id': [
#                     'Not a valid integer value.',
#                     'Not a valid integer value.'
#             ]},
#                 resp.json['errors']
#             )

# # TODO: fail create new experience for non-existent user admin
#     def test_create_user_experience_fail_invalid_user_admin(self):
#         """Admin can NOT create an experience for a user that doesn't exist"""

#         invalid_user = {
#             "date": datetime(year=2022, month=1, day=20).isoformat(),
#             "sign_in_time": datetime(year=2022, month=1, day=20, hour=12).isoformat(),
#             "department": "lab",
#             "user_id": 9999
#         }

#         with self.client as c:
#             resp = c.post(
#                     f"/users/{self.u2_id}/experiences",
#                     headers={"AUTHORIZATION": f"Bearer {self.admin_token}"},
#                     json=invalid_user
#             )

#             self.assertEqual(resp.status_code, 404)
#             self.assertIn("User not found", resp.json['errors'])

# # TODO: fail route does not match user_id provided in json data same user



# # TODO: fail route does not match user_id provided in json data admin


# # TODO: fail create new experience diff user
#     def test_create_user_experience_fail_diff_user(self):
#         """User can NOT create an experience for another user"""

#         experience_data = {
#             "date": datetime(year=2022, month=1, day=8).isoformat(),
#             "sign_in_time": datetime(year=2022, month=1, day=8, hour=12).isoformat(),
#             "department": "pharmacy",
#             "user_id": self.u2_id
#         }

#         with self.client as c:
#             resp = c.post(
#                     f"/users/{self.u2_id}/experiences",
#                     headers={"AUTHORIZATION": f"Bearer {self.u1_token}"},
#                     json=experience_data
#             )

#             self.assertEqual(resp.status_code, 401)
#             self.assertEqual(resp.json['errors'], "Unauthorized")

# # TODO: fail create new experience no token
#     def test_create_user_experience_fail_no_token(self):
#         """Can NOT create an experience without token"""

#         experience_data = {
#             "date": datetime(year=2022, month=1, day=8).isoformat(),
#             "sign_in_time": datetime(year=2022, month=1, day=8, hour=12).isoformat(),
#             "department": "pharmacy",
#             "user_id": self.u2_id
#         }

#         with self.client as c:
#             resp = c.post(
#                     f"/users/{self.u2_id}/experiences",
#                     json=experience_data
#             )

#             self.assertEqual(resp.status_code, 401)
#             self.assertIn("Missing JWT", resp.json['msg'])

# # TODO: fail create new experience invalid token
#     def test_create_user_experience_fail_invalid_token(self):
#         """Can NOT create an experience with invalid token"""

#         experience_data = {
#             "date": datetime(year=2022, month=1, day=8).isoformat(),
#             "sign_in_time": datetime(year=2022, month=1, day=8, hour=12).isoformat(),
#             "department": "pharmacy",
#             "user_id": self.u2_id
#         }

#         with self.client as c:
#             resp = c.post(
#                     f"/users/{self.u2_id}/experiences",
#                     headers={"AUTHORIZATION": f"Bearer {BAD_TOKEN}"},
#                     json=experience_data
#             )

#             self.assertEqual(resp.status_code, 401)
#             self.assertEqual(resp.json['errors'], "Invalid token")


########################################################################
# PATCH /users/<user_id>/experiences/<exp_id> tests

# TODO: success update experience same user

# TODO: success update experience admin

# TODO: update experience does not update other data (besides sign out/dept) same user

# TODO: update experience does not update other data (besides sign out/dept) admin

# TODO: fail update experience missing sign out time same user

# TODO: fail update experience missing sign out time admin

# TODO: fail update experience diff user

# TODO: fail update experience no token

# TODO: fail update experience invalid token