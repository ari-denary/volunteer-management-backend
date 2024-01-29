import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models.models import connect_db
from flask_cors import CORS
from flask_jwt_extended import (
    verify_jwt_in_request,
    JWTManager
)
from models.User import User
from routes.users import users
from routes.auth import auth
from routes.experiences import experiences

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

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()

@app.before_request
def verify_jwt():
    """
    Check that a token is valid, if it is provided.
    Token is optional in this route - authentication only.
    If invalid token received, returns JSON:
    { "errors": "Invalid token" }
    """

    try:
        jwt = verify_jwt_in_request(locations=['headers', 'cookies'], optional=True)
        print("JWT VERIFIED as ", jwt)
    except Exception:
        return jsonify(errors="Invalid token"), 401


app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(users, url_prefix="/users")
app.register_blueprint(experiences, url_prefix="/experiences")

