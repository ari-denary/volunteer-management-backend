from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user
from models.User import User
from models.Experience import Experience
from forms.CreateExperienceForm import CreateExperienceForm
from models.models import db

experiences = Blueprint(
    "experiences",
    __name__,
    static_folder="../static",
    template_folder="../templates"
)

@experiences.get('')
@jwt_required(optional=False, locations=['headers', 'cookies'])
def get_all_experiences():
    """
    Gets all experiences for all users. Optional query parameter of 'incomplete'
    will return all experiences whose sign_out_time is None.
    Primary use case for 'incomplete' is to check any experiences that have not "signed out".
    Authorization: must be admin requesting with valid token.
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

    if (current_user.is_admin):
        if 'incomplete' in request.args:
            experiences = Experience.query.filter_by(
                sign_out_time=None
            ).all()
        else:
            experiences = Experience.query.all()

        serialized_experiences = [e.serialize() for e in experiences]

        return jsonify(experiences=serialized_experiences)

    return jsonify(errors="Unauthorized"), 401

@experiences.post('/<int:user_id>/experiences')
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

# @experiences.patch('/<int:user_id>/experiences/<int:exp_id>')
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