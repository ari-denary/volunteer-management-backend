from flask_wtf import FlaskForm
from wtforms import (
    StringField, IntegerField, DateTimeField
)
from wtforms.validators import InputRequired, Optional


class ClockInForm(FlaskForm):
    """
    Form for validation of incoming JSON data for updating an Experience
    with the sign out and optionally, department
    """

    class Meta:
        csrf = False

    user_id = IntegerField(
        "User id",
        validators=[InputRequired()]
    )

    department = StringField(
        "Department",
        validators=[Optional()]
    )

    sign_out_time = DateTimeField(
        "Sign Out Time",
        validators=[InputRequired()]
    )