from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler
from flask_moment import Moment
import os

app = Flask(__name__)
moment = Moment(app)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


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