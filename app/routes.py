from flask import render_template, flash, redirect, url_for, request, send_file, send_from_directory, safe_join, abort
from app import app, db
from app.forms import LoginForm, ApplyForm, ContactForm, MaintenanceForm, EventForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post, Event
import os
from werkzeug.utils import secure_filename
import smtplib


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
    posts = Post.query.order_by('timestamp')
    return render_template('maintenance.html', posts=posts)

@app.route('/maintenance_form', methods=['GET', 'POST'])
@login_required
def maintenance_form():
    form = MaintenanceForm()
    print(form.validate_on_submit())
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
    print(form.validate_on_submit())
    if form.validate_on_submit():
        event = Event(title=form.title.data, body=form.body.data, author=form.author.data, dateOfEvent=form.dateOfEvent.data, start=form.start_at.data, end=form.end_at.data)
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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invlaid username or password')
            return redirect('login')
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('home'))
    return render_template('login.html', title='Sign In', form=form)


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


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        email=form.email.data
        name=form.firstName.data + "" +form.lastName.data
        phone=form.phone.data
        message=form.message.data

        messageToUser="We have recieved your question and will respond soon."
        resultOfTheForm = "Name:"+name+"\nEmail:"+email+"\nPhone Number:"+phone+"\nMessage:"+message
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("fieldstonprojects@gmail.com", "Qwerty123!")
        server.sendmail("fieldstonprojects@gmail.com",email,resultOfTheForm)
        server.sendmail("fieldstonprojects@gmail.com","fieldstonprojects@gmail.com",resultOfTheForm)
        flash('Message Sent')
        return redirect(url_for('index'))

    return render_template('contact.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
