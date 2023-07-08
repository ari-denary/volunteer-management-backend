from flask_wtf import FlaskForm
from wtforms import (
    StringField, DateTimeField
)
from wtforms.validators import InputRequired, Optional


class UpdateExperienceForm(FlaskForm):
    """
    Form for validation of incoming JSON data for updating an Experience
    with sign out time and optionally, department
    """

    class Meta:
        csrf = False

    sign_out_time = DateTimeField(
        "Sign Out Time",
        validators=[InputRequired()],
        format="%Y-%m-%dT%H:%M:%S.%f",
    )

    department = StringField(
        "Department",
        validators=[Optional()]
    )