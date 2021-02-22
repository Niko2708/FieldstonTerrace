from flask_wtf import FlaskForm, validators
from app.models import User
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField, SelectField, FileField
from wtforms.fields.html5 import DateField, TimeField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('First Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class MaintenanceForm(FlaskForm):
    title = StringField('Title:', validators=[DataRequired()])
    body = TextAreaField('Body:', validators=[DataRequired()])
    date = DateField('Date of Event:', validators=[DataRequired()])
    start_at = TimeField('Start at')
    end_at = TimeField('End at')
    submit = SubmitField('Submit')

class EventForm(FlaskForm):
    title = StringField('Title:', validators=[DataRequired()])
    body = TextAreaField('Body:', validators=[DataRequired()])
    dateOfEvent = DateField('Date of Event:', validators=[DataRequired()])
    start_at = TimeField('Start at', validators=[DataRequired()])
    end_at = TimeField('End at', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

class ChangePasswordForm(FlaskForm):
    currentPassword = PasswordField('Password', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

class CommunityBoardForm(FlaskForm):
    post = TextAreaField('Body:', validators=[DataRequired()])
    submit = SubmitField('Post')

class EditUsernameForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Save')

class EditNameForm(FlaskForm):
    firstName = StringField('First Name')
    lastName = StringField('First Name')
    submit = SubmitField('Submit')