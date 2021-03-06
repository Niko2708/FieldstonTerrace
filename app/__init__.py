from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler
from flask_moment import Moment
from flask_mail import Mail, Message
import os
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from flask_bootstrap import Bootstrap

#Error logging and tracking using sentry.io
sentry_sdk.init(
    dsn="https://f025b238b1c34b4aa261c1ae646fe445@o508992.ingest.sentry.io/5602555",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)

app = Flask(__name__)
# A javascript library that customs time and dates
moment = Moment(app)
Bootstrap(app)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config["TEMPLATES_AUTO_RELOAD"] = True

#for database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)

#for login pages
login = LoginManager(app)
login.login_view = 'login'

#for downloadable files
app.config["CLIENT_PDF"] = "static/pdf"
app.config["PDF_UPLOADS"] = "/Users/Family/PycharmProjects/FieldstonProject/app/static/applicationSubmissions"
app.config["ALLOWED_EXTENSIONS"] = ["PDF"]
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 *10224

from app import routes, models