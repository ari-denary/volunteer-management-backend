from flask import Blueprint, jsonify, request
from models.models import db
from flask_jwt_extended import create_access_token
from models.User import User
from forms.LoginForm import LoginForm
from forms.SignUpForm import SignUpForm

auth = Blueprint(
    "auth",
    __name__,
    static_folder="../static",
    template_folder="../templates"
)

signup_schema = {
    "type": "object",
    "properties": {
        "badge_number": {"type": "string"},
        "email": {"type": "string"},
        "password": {"type": "string"},
        "first_name": {"type": "string"},
        "last_name": {"type": "string"},
        "dob": {
            "type": "string",
            "format": "date-time",
            "title": "dob",
            "description": "Datetime in the format '2022-06-12T14:30:00'",
            "example": "2022-06-12T14:30:00"
        },
        "address": {"type": "string"},
        "city": {"type": "string"},
        "state": {"type": "string"},
        "zip_code": {"type": "string"},
        "phone_number": {"type": "string"},
        "is_student": {"type": "boolean"},
        "is_multilingual": {"type": "boolean"},
    },
    "required": [
        "badge_number",
        "email",
        "password",
        "first_name",
        "last_name",
        "dob",
        "address",
        "city",
        "state",
        "zip_code",
        "phone_number",
        "is_student",
    ]
}

@auth.post("/signup")
def signup():
    """
    Handle user signup.
    Expecting JSON: {
        "badge_number":"1",
        "email":"sample@mail.com",
        "password":"password",
        "first_name":"sample",
        "last_name":"user",
        "dob":"datetime.datetime(2000, 1, 1, 0, 0)",
        "gender":"Prefer not to say",
        "address":"123 Cherry lane",
        "city":"New York",
        "state":"NY",
        "zip_code":"11001",
        "phone_number":"9991234567",
        "is_student":"true",
        "is_multilingual":"false"
    }
    Returns JSON: { "token": "dleoidlksd.aslkfjoiweflkfj.aldsjfoweifsldf" }
    """

    received = request.json

    form = SignUpForm(csrf_enabled=False, data=received)

    if form.validate_on_submit():
        user = User.signup(
            badge_number=received.get("badge_number"),
            email=received.get("email"),
            password=received.get("password"),
            first_name=received.get("first_name"),
            last_name=received.get("last_name"),
            dob=received.get("dob"),
            gender=received.get("gender"),
            address=received.get("address"),
            city=received.get("city"),
            state=received.get("state"),
            zip_code=received.get("zip_code"),
            phone_number=received.get("phone_number"),
            is_student=received.get("is_student"),
            is_multilingual=received.get("is_multilingual")
        )

        try:
            db.session.commit()

            # Note: payload is stored on "sub" of token
            token = create_access_token(identity=user)
            return jsonify(token=token)

        except Exception:
            return jsonify(
                errors="Invalid data: email or badge number already in use"
            )

    return jsonify(errors=form.errors), 400


@auth.post("/login")
def login():
    """
    Handle user login.
    Expecting JSON: { "email": "mail@mail.com", "password": "mypassword" }
    Returns JSON:
    - If provided valid data:
    { "token": "dleoidlksd.aslkfjoiweflkfj.aldsjfoweifsldf" }
    - If provided invalid data:
    { "errors": "Invalid credentials" }
    """

    received = request.json

    form = LoginForm(csrf_enabled=False, data=received)

    if form.validate_on_submit():
        user = User.authenticate(
            email=received.get("email"),
            password=received.get("password")
        )

        if user:
            # Note: payload is stored on "sub" of token
            token = create_access_token(identity=user)
            return jsonify(token=token)

    return jsonify(errors="Invalid credentials"), 400