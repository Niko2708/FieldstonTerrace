from flask_wtf import FlaskForm, validators
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField, SelectField, FileField
from wtforms.fields.html5 import DateField, TimeField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ApplyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    residenceType = SelectField('Residence Type', choices=[('One Bedroom'), ('Two Bedroom'), ('Three Bedroom')], validators=[DataRequired()])
    desiredMoveInDate =SelectField('Desired Move in Data', choices=[('January'), ('February'),('March'), ('April'),('May'),('June'), ('July'),('August'),('September'),('October'),('November'),('December')], validators=[DataRequired()])
    applicationForm = FileField('Application Form')
    submit = SubmitField('submit')

class MaintenanceForm(FlaskForm):
    title = StringField('Title:', validators=[DataRequired()])
    body = TextAreaField('Body:', validators=[DataRequired()])
    author = StringField('Name')
    date = DateField('Date of Event:', validators=[DataRequired()])
    start_at = TimeField('Start at', validators=[DataRequired()])
    end_at = TimeField('End at', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EventForm(FlaskForm):
    title = StringField('Title:', validators=[DataRequired()])
    body = TextAreaField('Body:', validators=[DataRequired()])
    author = StringField('Name:', validators=[DataRequired()])
    dateOfEvent = DateField('Date of Event:', validators=[DataRequired()])
    location = StringField('Location')
    start_at = TimeField('Start at', validators=[DataRequired()])
    end_at = TimeField('End at', validators=[DataRequired()])
    submit = SubmitField('Submit')