from flask_wtf import FlaskForm, validators
from app.models import User
from sqlalchemy import func
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField, SelectField, FileField
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
    profile_pic= FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
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
            user = User.query.filter_by(phone_number=phone.data).first()
            if user is not None:
                raise ValidationError('Phone number is already associated with an account.')
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

    def validate_password(self, password):
        if len(password.data) >= 7 and len(password.data) <= 20:
            raise ValidationError('Password needs to be between 7 and 20 characters')

class MaintenanceForm(FlaskForm):
    title = StringField('Title:', validators=[DataRequired()])
    body = TextAreaField('Body:', validators=[DataRequired()])
    img = FileField('Post pic', validators=[FileAllowed(['jpg', 'png'])])
    date = DateField('Date of Event:', validators=[DataRequired()])
    start_at = TimeField('Start at')
    end_at = TimeField('End at')
    submit = SubmitField('Submit')

class EventForm(FlaskForm):
    title = StringField('Title:', validators=[DataRequired()])
    body = TextAreaField('Body:', validators=[DataRequired()])
    img = FileField('Post pic', validators=[FileAllowed(['jpg', 'png'])])
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
    title = TextAreaField('Title', validators=[DataRequired()])
    post = TextAreaField('Body:', validators=[DataRequired()])
    post_img = FileField('Post pic', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post')

class EditUsernameForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Save')

class EditNameForm(FlaskForm):
    firstName = StringField('First Name')
    lastName = StringField('First Name')
    submit = SubmitField('Submit')

class ChangeEmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ChangePhoneForm(FlaskForm):
    phone = phone = StringField('Phone', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_phone(self, phone):
        try:
            p = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')