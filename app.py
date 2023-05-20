import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models.models import db, connect_db
from flask_cors import CORS, cross_origin, logging
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity,
    verify_jwt_in_request,
    JWTManager
)
from models.User import User
from forms.LoginForm import LoginForm

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
    """

    verify_jwt_in_request(locations=['headers', 'cookies'], optional=True)


@app.post("/login")
def login():
    """
    Handle user login.
    Expecting JSON: { "email": "mail@mail.com", "password": "mypassword" }
    Returns JSON: { "token": "dleoidlksd.aslkfjoiweflkfj.aldsjfoweifsldf" }
    """

    received = request.json

    form = LoginForm(csrf_enabled=False, data=received)

    if form.validate_on_submit():
        user = User.authenticate(
            email=request.json.get("email"),
            password=request.json.get("password")
        )

        # Note: payload is stored on "sub" of token
        token = create_access_token(identity=user.id)
        return jsonify(token=token)

    else:
        return jsonify(errors=form.errors)