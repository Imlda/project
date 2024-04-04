from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, EmailField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from application.utils import exists_email, not_exists_email, exists_username

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SignUpForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=12), exists_username])
    fullname = StringField("Full Name", validators=[DataRequired(), Length(min=4, max=16)])
    email = EmailField("Email", validators=[DataRequired(), Email(), exists_email])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=4)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), Length(min=4), EqualTo("password")])
    submit = SubmitField("Sign Up")

class ResetPasswordForm(FlaskForm):
    old_pass = PasswordField("Old Password", validators=[DataRequired(), Length(min=4)])
    new_pass = PasswordField("New Password", validators=[DataRequired(), Length(min=4)])
    confirm_pass = PasswordField("Confirm New Password", validators=[DataRequired(), Length(min=4), EqualTo("new_pass")])
    submit = SubmitField("Reset Password")

class ForgotPasswordForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), not_exists_email])
    recaptcha = RecaptchaField()
    submit = SubmitField("Send Verification Link")

class VerificationForm(FlaskForm):
    password = PasswordField("New Password", validators=[DataRequired(), Length(min=4)])
    confirm_password = PasswordField("Confirm New Password", validators=[DataRequired(), Length(min=4), EqualTo("password")])
    submit = SubmitField("Reset Password")
