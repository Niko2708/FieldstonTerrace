from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler

app = Flask(__name__)
app.config.from_object(Config)

#for database
db=SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)

#for login pages
login = LoginManager(app)
login.login_view = 'login'

#for downloadable files
app.config["CLIENT_PDF"] = "/Users/Family/PycharmProjects/FieldstonProject/app/static/pdf"
app.config["PDF_UPLOADS"] = "/Users/Family/PycharmProjects/FieldstonProject/app/static/applicationSubmissions"
app.config["ALLOWED_EXTENSIONS"] = ["PDF"]
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 *10224

from app import routes, models

#email server
if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)