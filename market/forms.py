from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, DataRequired, Email


class RegisterForm(FlaskForm):
    username = StringField(label="User Name", validators=[DataRequired(), Length(min=2, max=30)])
    email_address = EmailField(label="Email Address", validators=[DataRequired(), Email()])
    password1 = PasswordField(label="Password", validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField(label="Confirm Password", validators=[DataRequired(), EqualTo("password1")])
    submit = SubmitField(label="Create Account")
