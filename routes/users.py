from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user
from models.User import User
from models.Experience import Experience

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

