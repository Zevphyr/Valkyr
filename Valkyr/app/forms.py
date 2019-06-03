from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Valkyr.app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # fill in after we implement database feature
    def validate_username(self, username):
        # if user is none then it will proceed to add the new account to the database
        user = User.query.filter_by(username=username.data).first()
        # if user exists then it will raise a Validation error
        if user:
            raise ValidationError('The username is taken. Please choose a different one.')

    def validate_email(self, email):
        # if email is none then it will skip the conditional and the new account to the database
        email = User.query.filter_by(email=email.data).first()
        # if email exists then it will raise a ValidationError
        if email:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')

    # fill in after we implement database feature
    def validate_username(self, username):
        pass

    def validate_email(self, email):
        pass