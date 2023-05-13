import os
from dotenv import load_dotenv

from flask import (
    Flask, request, jsonify, session
)

# Import DebugToolbarExtension class
from flask_debugtoolbar import DebugToolbarExtension

from models.models import db, connect_db

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
debug = DebugToolbarExtension(app)  # debug

# from sqlalchemy.exc import IntegrityError
# CURR_USER_KEY = "curr_user"