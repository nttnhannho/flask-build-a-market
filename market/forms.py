from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, DataRequired, Email, ValidationError
from market.models import User


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError("User name is already existed! Please use different user name.")

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError("Email_address is already existed! Please use different email_address.")

    username = StringField(label="User Name", validators=[DataRequired(message="User name is required"), Length(min=2, max=30, message="User name length should be from 2 to 30")])
    email_address = EmailField(label="Email Address", validators=[DataRequired(message="Email address is required"), Email(message="Email should be valid format")])
    password = PasswordField(label="Password", validators=[DataRequired(message="Password is required"), Length(min=8, message="Password length should be at least 8 characters")])
    confirm_password = PasswordField(label="Confirm Password", validators=[DataRequired(message="Confirm password is required"), EqualTo("password", message="Passwords do not match")])
    submit = SubmitField(label="Create Account")


class LoginForm(FlaskForm):
    username = StringField(label="User Name", validators=[DataRequired(message="User name is required")])
    password = PasswordField(label="Password", validators=[DataRequired(message="Password is required")])
    submit = SubmitField(label="Log In")
