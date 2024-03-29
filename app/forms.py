from flask_wtf import FlaskForm, validators
from app.models import User
from sqlalchemy import func
from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField, SelectField
from wtforms.fields.html5 import DateField, TimeField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from flask_wtf.file import FileField, FileAllowed
import phonenumbers

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    profile_pic= FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png','jpeg'])])
    phone = StringField('Phone')
    email_notification = BooleanField('Text Notification', default=False)
    mobile_notification = BooleanField('Mobile Notification', default=False)
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=14)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_phone(self, phone):
        try:
            p = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')

    def validate_username(self, username):
        user = User.query.filter(func.lower(User.username) == func.lower(username.data)).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class CommunityBoardForm(FlaskForm):
    title = TextAreaField('Title', validators=[DataRequired()])
    post = TextAreaField('Body:', validators=[DataRequired()])
    post_img = FileField('Post pic', validators=[FileAllowed(['jpg', 'png','pdf'])])
    submit = SubmitField('Post')

class MaintenanceForm(FlaskForm):
    title = StringField('Title:', validators=[DataRequired()])
    body = TextAreaField('Body:', validators=[DataRequired()])
    img = FileField('Post pic', validators=[FileAllowed(['jpeg', 'png', 'jpg'])])
    submit = SubmitField('Submit')

class EventForm(FlaskForm):
    title = StringField('Title:', validators=[DataRequired()])
    body = TextAreaField('Body:', validators=[DataRequired()])
    img = FileField('Post pic', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Submit')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

class EditUsernameForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Save')

class ChangeProfilePicture(FlaskForm):
    profile_img = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png','jpeg'])])
    submit = SubmitField('Updated Profile Picture')

class ChangePasswordForm(FlaskForm):
    currentPassword = PasswordField('Password', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[EqualTo('password')])
    submit = SubmitField('Request Password Reset')

class EditNameForm(FlaskForm):
    firstName = StringField('First Name')
    lastName = StringField('Last Name')
    submit = SubmitField('Submit')

class ChangeEmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class ChangeContactForm(FlaskForm):
    phone = StringField('Phone')
    email_notification = BooleanField('Text Notification')
    mobile_notification = BooleanField('Mobile Notification')
    submit = SubmitField('Submit')

    def validate_phone(self, phone):
        try:
            p = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')