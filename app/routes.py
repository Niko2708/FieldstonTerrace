from flask import render_template, flash, redirect, url_for, request, send_file, send_from_directory, safe_join, abort
from app import app, db, mail
from app.forms import LoginForm, MaintenanceForm, EventForm, RegistrationForm, ResetPasswordRequestForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post, Event
from app.email import send_password_reset_email
import os
from werkzeug.utils import secure_filename
import smtplib
from flask_mail import Message
from app.forms import ResetPasswordForm

# routes for resident users that login in
@app.route('/home')
@login_required
def home():
    posts = Post.query.order_by('timestamp').limit(4)
    events = Event.query.order_by('timestamp').limit(4)
    return render_template('home.html', posts=posts, events=events)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/events')
@login_required
def events():
    events = Event.query.order_by('timestamp').limit(4)
    return render_template('events.html',events=events)

@app.route('/documents')
def documents():
    print("Hello World!")
    return render_template('documents.html')


@app.route("/get_pdf/<filename>")
def get_pdf(filename):
    print(filename)
    try:
        return send_from_directory(app.config["CLIENT_PDF"], filename=filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)

@app.route('/maintenance', methods=['GET','POST'])
@login_required
def maintenance():
    posts = Post.query.order_by(Post.date.desc())
    return render_template('maintenance.html', posts=posts)

@app.route('/maintenance_form', methods=['GET', 'POST'])
@login_required
def maintenance_form():
    form = MaintenanceForm()

    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, start=form.start_at.data, end=form.end_at.data, date=form.date.data)
        db.session.add(post)
        db.session.commit()
        flash('Maintenance Form Successful')
        return redirect(url_for('home'))
    return render_template('maintenance_form.html', title='Maintenance Report', form=form)

@app.route('/event_form', methods=['GET', 'POST'])
@login_required
def event_form():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(title=form.title.data, body=form.body.data, dateOfEvent=form.dateOfEvent.data, start=form.start_at.data, end=form.end_at.data)
        db.session.add(event)
        db.session.commit()
        flash('Maintenance Form Successful')
        return redirect(url_for('home'))
    return render_template('event_form.html', form=form)

# routes for non resident users
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/amenities')
def amenities():
    return render_template('amenities.html')


@app.route('/neighborhood')
def neighborhood():
    return render_template('neighborhood.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            error = 'There is no user with that username'
            return render_template('login.html', error = error, form = form)
        elif not user.check_password(form.password.data):
            error = 'Wrong password. Try again or click Forgot password to rest it'
            return render_template('login.html', error = error, form=form)
        else:
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('home'))
    return render_template('login.html', form=form)


@app.route('/apply', methods=['GET', 'POST'])
def apply():
    def allowed_pdf(filename):
        if not "." in filename:
            return False

        ext = filename.rsplit(".", 1)
        if ext[1].upper() in app.config["ALLOWED_EXTENSIONS"]:
            return True
        else:
            return False

    """""
    def allowed_pdf_filesize(filesize):
        if int(filesize) <= app.config["MAX_CONTENT_LENGTH"]:
            return True
        else:
            return False
    """
    if request.method == "POST":
        if request.files:
            """
            if not allowed_pdf_filesize(request.cookies["filesize"]):
                print("Filesize exceeded maximum limit")
                return redirect(request.url)
            """

            pdf = request.files["pdf"]

            if pdf.filename == "":
                print("No filename")
                return redirect(request.url)

            if allowed_pdf(pdf.filename):
                filename = secure_filename(pdf.filename)
                pdf.save(os.path.join(app.config["PDF_UPLOADS"], filename))
                print("PDF saved")
                return redirect(request.url)

            else:
                print("That file extensions is not allowed")
                return redirect(request.url)

    form = ApplyForm()
    # if form.validate_on_submit():
    # return redirect('/')
    return render_template('apply.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, firstName=form.firstName.data, lastName=form.lastName.data, email=form.email.data, phoneNumber=form.phone.data)
        #need to add something to clean up phone number
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)
    
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run()