from flask_wtf import FlaskForm
from wtforms import (
    StringField, IntegerField, DateTimeField
)
from wtforms.validators import InputRequired, Optional


class ClockInForm(FlaskForm):
    """Form for validation of incoming JSON data for adding a new Experience"""

    class Meta:
        csrf = False

    user_id = IntegerField(
        "User id",
        validators=[InputRequired()]
    )

    department = StringField(
        "Department",
        validators=[InputRequired()]
    )

    sign_out_time = DateTimeField(
        "Sign Out Time",
        validators=[Optional()]
    )