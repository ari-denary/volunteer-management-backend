import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models.models import db, connect_db
from flask_cors import CORS, cross_origin
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity,
    verify_jwt_in_request,
    JWTManager
)
from models.User import User
from forms.LoginForm import LoginForm
from forms.SignUpForm import SignUpForm

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# enable cors
CORS(app)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]
jwt = JWTManager(app)

connect_db(app)
debug = DebugToolbarExtension(app)  # debug

# from sqlalchemy.exc import IntegrityError

@app.before_request
def verify_jwt():
    """
    Check that a token is valid, if it is provided.
    Token is optional in this route - authentication only.
    If invalid token received, returns JSON:
    { "errors": "Invalid token" }
    """

    try:
        verify_jwt_in_request(locations=['headers', 'cookies'], optional=True)
    except Exception:
        return jsonify(errors="Invalid token")

@app.post("/signup")
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
            token = create_access_token(identity=user.id)
            return jsonify(token=token)

        except Exception:
            return jsonify(
                errors="Invalid data: email or badge number already in use"
            )

    return jsonify(errors=form.errors)


@app.post("/login")
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
            token = create_access_token(identity=user.id)
            return jsonify(token=token)

    return jsonify(errors="Invalid credentials")