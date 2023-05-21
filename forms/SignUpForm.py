from flask_wtf import FlaskForm
from wtforms import (
    StringField, DateTimeField, BooleanField, PasswordField, EmailField, IntegerField
)
from wtforms.validators import InputRequired, Email, ValidationError
from datetime import datetime
from dateutil import relativedelta

def over_18():
    message = 'You must be 18 years or older to volunteer'

    def _over_18(form, field):
        naive_today = datetime.today()
        naive_dob = datetime(field.data)
        diff = relativedelta(naive_today, naive_dob)

        if diff.years < 18:
            raise ValidationError(message)

    return _over_18

class SignUpForm(FlaskForm):
    """Form for validation of incoming JSON data for signing up a User"""

    class Meta:
        csrf = False

    badge_number = IntegerField(
        "Badge Number",
        validators=[InputRequired()]
    )

    email = EmailField(
        "Email",
        validators=[InputRequired(), Email()]
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired()]
    )

    first_name = StringField(
        "Last name",
        validators=[InputRequired()]
    )

    last_name = StringField(
        "First name",
        validators=[InputRequired()]
    )

    dob = DateTimeField(
        "Date of Birth",
        validators=[InputRequired()]
    )

    gender = StringField(
        "gender",
        validators=[InputRequired()]
    )

    address = StringField(
        "Address",
        validators=[InputRequired()]
    )

    city = StringField(
        "City",
        validators=[InputRequired()]
    )

    state = StringField(
        "State",
        validators=[InputRequired()]
    )

    zip_code = StringField(
        "Zip code",
        validators=[InputRequired()]
    )

    phone_number = StringField(
        "Phone number",
        validators=[InputRequired()]
    )

    is_student = BooleanField(
        "Is a student?",
        validators=[InputRequired()]
    )

    is_multilingual = BooleanField(
        "Speaks another language?",
        validators=[]
    )
