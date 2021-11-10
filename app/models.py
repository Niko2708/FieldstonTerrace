from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from time import time
import jwt
from app import app

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    phone_number = db.Column(db.String())
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_img = db.Column(db.String(20), default='default.jpeg')
    password_hash = db.Column(db.String(128), nullable=False)
    email_notification = db.Column(db.Boolean, default=False)
    text_notification = db.Column(db.Boolean, default=False)
    posts = db.relationship('CommunityBoard', backref='author', lazy=True)
    maintenances = db.relationship('Maintenance', backref='author', lazy=True)
    events = db.relationship('Event', backref='author', lazy=True)
    admin = db.Column(db.Boolean, default=False)


    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    # the id is encode so that we can find the user
    # the password_hash is encode so that when password is reset the token will no longer be valid.
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset': self.id, 'password': self.password_hash, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset']

            hash = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['password']
        except:
            return

        user = User.query.filter_by(id=id).first()

        if user and user.password_hash == hash:
            return User.query.get(user.id)
        else:
            return

class Maintenance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    maintenance_img = db.Column(db.String(20))
    title = db.Column(db.String(120))
    body = db.Column(db.String)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_img = db.Column(db.String(20), nullable=False, default='default.jpg')
    title = db.Column(db.String(120))
    body = db.Column(db.String)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class CommunityBoard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    post_img = db.Column(db.String(20), nullable=True)
    body = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


def get_registration_token(email, expires_in=86400):
    return jwt.encode(
        {'register_user':email, 'exp': time() + expires_in},
        app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')


def verify_registration_token(token):
    try:
        id = jwt.decode(token, app.config['SECRET_KEY'],
                        algorithms=['HS256'])['register_user']
    except:
        return
    return User.query.get(id)
