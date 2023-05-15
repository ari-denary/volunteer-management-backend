from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField
from wtforms.validators import InputRequired, Email

class LoginForm(FlaskForm):
    """Form for validation of incoming JSON data for logging in a User"""

    class Meta:
        csrf = False

    email = EmailField(
        "Email",
        validators=[InputRequired(), Email()]
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired()]
    )