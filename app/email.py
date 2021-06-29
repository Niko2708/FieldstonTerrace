from app import app
from app.forms import RegistrationForm
from flask import render_template
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from time import time
import jwt
import os

sender = 'fieldstontowers@gmail.com'


def send_maintenance_post(users, post):
    for user in users:
        print(user.username)
        print(user.email_notification)
        if user.email_notification:
            test = Mail(
                from_email=sender,
                to_emails=user.email,
                subject=post.title,
                html_content=render_template('email/maintenance_email.html', post=post))
            try:
                sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                response = sg.send(test)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(e)


def send_password_change_confirmation(user, recipient):
    message = Mail(
        from_email=sender,
        to_emails=recipient,
        subject='Password Change Confirmation',
        html_content=render_template('email/password_change.html', user=user))
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)


def send_password_reset_email(user, to_email):
    token = user.get_reset_password_token()
    message = Mail(
        from_email=sender,
        to_emails=to_email,
        subject='Password Restart link',
        html_content=render_template('email/reset_password.html', user=user, token=token))
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)


def get_registration_token(expires_in=86400):
    return jwt.encode(
        {'register_user': 'test', 'exp': time() + expires_in},
        app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')


def verify_registration_token(token):
    try:
        code = jwt.decode(token, app.config['SECRET_KEY'],
                          algorithms=['HS256'])['register_user']
    except:
        return
    return code


def send_user_registeration_email(to_email):
    token = get_registration_token()
    form = RegistrationForm()
    message = Mail(
        from_email=sender,
        to_emails=to_email,
        subject='Registeration Link',
        html_content=render_template('email/register.html', form=form, token=token))
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)


def send_unknow_user_email(recipient):
    message = Mail(
        from_email=sender,
        to_emails=recipient,
        subject='Password Reset',
        html_content=render_template('email/unknow_user.html'))
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
