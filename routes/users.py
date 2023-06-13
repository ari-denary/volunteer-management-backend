from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user
from models.User import User
from models.Experience import Experience
from forms.CreateExperienceForm import CreateExperienceForm
from models.models import db

users = Blueprint(
    "users",
    __name__,
    static_folder="../static",
    template_folder="../templates"
)

@users.get('')
@jwt_required(optional=False, locations=['headers', 'cookies'])
def get_users():
    """
    Gets all users.
    Authorization: must be admin requesting with valid token.
    Returns JSON {
        users: [{
            "id": 1,
            "email": "admin@mail.com",
            "experience_hours": 10
            "badge_number": 100,
            "first_name": "first",
            "last_name": "user",
            "is_admin": False,
            "is_student": True,
            "is_multilingual": False,
            "status": "new"
        } ... ]
    }
    If unauthorized request, returns JSON { "errors": "Unauthorized" }
    """

    if (current_user.is_admin):
        user_instances = User.query.all()
        users = []
        for u in user_instances:
            user_experiences = Experience.query.filter_by(user_id=u.id).all()
            experience_hours = 0
            for exp in user_experiences:
                experience_hours += exp.get_duration()

            users.append({
                "id": u.id,
                "badge_number": u.badge_number,
                "email": u.email,
                "experience_hours": experience_hours,
                "first_name": u.first_name,
                "is_admin": u.is_admin,
                "is_student": u.is_student,
                "is_multilingual": u.is_multilingual,
                "last_name": u.last_name,
                "status": u.status,
            })
        return jsonify(users=users)

    return jsonify(errors="Unauthorized"), 401

@users.get('/<int:user_id>')
@jwt_required(optional=False, locations=['headers', 'cookies'])
def get_user(user_id):
    """
    Gets a user by id.
    Authorization: must be same user or admin requesting with valid token.
    Returns JSON {
        user: {
            "id": 1,
            "email": "admin@mail.com",
            "badge_number": 100,
            "first_name": "first",
            "last_name": "user",
            "dob": "Sat, 01 Jan 2000 00:00:00 GMT",
            "gender": "Prefer not to say",
            "created_at": "Sun, 21 May 2023 20:12:14 GMT",
            "phone_number": "9991234567",
            "address": "123 Cherry lane",
            "city": "New York",
            "state": "NY",
            "zip_code": "11001"
            "is_admin": false,
            "is_multilingual": false,
            "is_student": true,
            "status": "new",
        }
    }
    If unauthorized request, returns JSON { "errors": "Unauthorized" }
    """

    if (current_user.id == user_id or current_user.is_admin):
        user = User.query.get_or_404(user_id)
        return jsonify(user=user.serialize())

    return jsonify(errors="Unauthorized"), 401


@users.get('/<int:user_id>/experiences')
@jwt_required(optional=False, locations=['headers', 'cookies'])
def get_user_experiences(user_id):
    """
    Gets all experiences for a user. Optional query parameter of 'incomplete'
    will return all experiences whose sign_out_time is None.
    Primary use case for 'incomplete' is for getting experience(s) to "sign out".
    Authorization: must be same user or admin requesting with valid token.
    Returns JSON {
        user_experiences: [{
            "id": 1,
            "date": "2023-04-06-08:35:12:23",
            "sign_in_time": "2023-04-06-08:35:12:23",
            "sign_out_time": "2023-04-06-08:35:12:23",
            "department": "lab",
            "user_id": 3
        } ... ]
    }
    If unauthorized request, returns JSON { "errors": "Unauthorized" }
    """

    if (current_user.id == user_id or current_user.is_admin):
        if 'incomplete' in request.args:
            experiences = Experience.query.filter_by(
                user_id=user_id
            ).filter_by(
                sign_out_time=None
            ).all()
        else:
            experiences = Experience.query.filter_by(user_id=user_id).all()

        user_experiences = [e.serialize() for e in experiences]

        return jsonify(user_experiences=user_experiences)

    return jsonify(errors="Unauthorized"), 401

@users.post('/<int:user_id>/experiences')
@jwt_required(optional=False, locations=['headers', 'cookies'])
def create_user_experience(user_id):
    """
    Create a new experience. Use case for "signing-in" to an experience.
    Authorization: must be same user or admin requesting with valid token.
    Accepts JSON - "date", "sign_in_time", "department", "user_id" required
                   "sign_out_time" optional
    {
        "date": "2022-01-05 00:00:00",
        "sign_in_time": "2022-01-05 08:00:00",
        "department": "lab",
        "user_id": 3
    }
    Returns JSON {
        user_experience: {
            "id": 1,
            "date": "2022-01-05 00:00:00",
            "sign_in_time": "2022-01-05 08:00:00",
            "sign_out_time": None,
            "department": "lab",
            "user_id": 3
        }
    }
    If unauthorized request, returns JSON { "errors": "Unauthorized" }
    """

    received = request.json

    form = CreateExperienceForm(csrf_enabled=False, data=received)

    if ((current_user.id == user_id and user_id == received['user_id'])
    or current_user.is_admin):
        if form.validate_on_submit():
            experience = Experience(
                date=received.get('date'),
                sign_in_time=received.get('sign_in_time'),
                sign_out_time=received.get('sign_out_time'),
                department=received.get('department'),
                user_id=received.get('user_id')
            )

            try:
                db.session.add(experience)
                db.session.commit()
                serialized = experience.serialize()
                return jsonify(user_experience=serialized)

            except Exception:
                print("EXCEPTION OCCURRED UPON DB COMMIT, experience = ", experience)
                return jsonify(errors="Database Error")

        return jsonify(errors=form.errors), 400

    return jsonify(errors="Unauthorized"), 401

# @users.patch('/<int:user_id>/experiences/<int:exp_id>')
# @jwt_required(optional=False, locations=['headers', 'cookies'])
# def update_user_experience(user_id, exp_id):
#     """
#     Update a user's experience sign out time and/or department.
#     Use case for "signing-out" of an experience.
#     Authorization: must be same user or admin requesting with valid token.
#     Accepts JSON - "sign_out_time" required,
#                    "department" optional
#     {
#         "sign_out_time": "2023-04-06-08:35:12:23",
#         "department": "pharmacy"
#     }
#     Returns JSON {
#         user_experience: {
#             id: 1,
#             date: "2023-04-06-08:35:12:23",
#             sign_in_time: "2023-04-06-08:35:12:23",
#             sign_out_time: "2023-04-06-08:35:12:23",
#             department: "pharmacy",
#             user_id: 3
#         }
#     }
#     If unauthorized request, returns JSON { "errors": "Unauthorized" }
#     """
