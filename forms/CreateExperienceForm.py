from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateTimeField
from wtforms.validators import InputRequired, Optional


class CreateExperienceForm(FlaskForm):
    """Form for validation of incoming JSON data for adding a new Experience"""

    class Meta:
        csrf = False

    date = DateTimeField(
        "date",
        validators=[InputRequired()],
        format="%Y-%m-%dT%H:%M:%S.%f",
    )

    sign_in_time = DateTimeField(
        "Sign In Time",
        validators=[InputRequired()],
        format="%Y-%m-%dT%H:%M:%S.%f",
    )

    sign_out_time = DateTimeField(
        "Sign Out Time",
        validators=[Optional()],
        format="%Y-%m-%dT%H:%M:%S.%f",
    )

    department = StringField(
        "Department",
        validators=[InputRequired(), ]
    )

    user_id = IntegerField(
        "User id",
        validators=[InputRequired()]
    )