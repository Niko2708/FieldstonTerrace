from flask import render_template, flash, redirect, url_for, request, send_file, send_from_directory, safe_join, abort
from app import app, db
from app.forms import *
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Maintenance, Event, CommunityBoard
from app.email import *
import os
import secrets


# routes for resident users that login in
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    image_file = url_for('static', filename='profile_pics/default.jpg')
    form = CommunityBoardForm()
    if form.validate_on_submit():
        picture_file = None
        if form.post_img.data:
            picture_file = save_picture(form.post_img.data, 1)

        posts = CommunityBoard(title=form.title.data, body=form.post.data, post_img=picture_file, author=current_user)
        db.session.add(posts)
        db.session.commit()
        flash('Post Successful')
    posts = CommunityBoard.query.order_by(CommunityBoard.timestamp.desc()).all()
    maintenance_post = Maintenance.query.order_by(Maintenance.timestamp.desc()).all()
    return render_template('home.html', form=form, posts=posts, maintenance_post=maintenance_post,
                           image_file=image_file)


@app.route("/maintenance/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_maintenance(post_id):
    post = Maintenance.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/maintenance/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def maintenance_update(post_id):
    post = Maintenance.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = MaintenanceForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        if form.img.data:
            picture_file = save_picture(form.img.data, 3)
            post.img = picture_file
        post.start = form.start_at.data
        post.end = form.end_at.data
        post.date = form.date.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.body.data = post.body
        form.start_at.data = post.start
        form.end_at.data = post.end
        form.date.data = post.date
    return render_template('maintenance_form.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = CommunityBoard.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = CommunityBoard.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = CommunityBoardForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.post.data
        if form.post_img.data:
            picture_file = save_picture(form.post_img.data, 1)
            post.post_img = picture_file
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.post.data = post.body
        form.post_img.data = post.post_img
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = CommunityBoard.query.filter_by(user_id=user.id).order_by(CommunityBoard.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts)

@app.route('/edit_profile/change_email', methods=['GET', 'POST'])
@login_required
def change_email():
    form = ChangeEmailForm()

    if form.validate_on_submit():
        current_user.email = form.email.data
        db.session.commit()
        render_template('/edit_profile.html')
    elif request.method == 'GET':
        form.email.data = current_user.email
    return render_template('editForm/email_edit.html', form=form)

@app.route('/edit_profile/change_contact_info', methods=['GET', 'POST'])
@login_required
def change_contact():
    form = ChangeContactForm()

    if form.validate_on_submit():
        current_user.phone_number = form.phone.data
        current_user.email_notification = form.email_notification.data
        current_user.text_notification = form.mobile_notification.data
        db.session.commit()
    elif request.method == 'GET':
        form.phone.data = current_user.phone_number
        form.email_notification.data = current_user.email_notification
        form.mobile_notification.data = current_user.text_notification
    return render_template('editForm/contact.html', form=form)


@app.route('/edit_profile/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    PasswordForm = ChangePasswordForm()

    if PasswordForm.validate_on_submit():
        if current_user.check_password(PasswordForm.currentPassword.data):
            current_user.set_password(PasswordForm.password.data)
            db.session.commit()
        elif not current_user.check_password(PasswordForm.password.data):
            error = 'Wrong password'
            return render_template('editForm/password.html', error=error, PasswordForm=PasswordForm)

    return render_template('editForm/password_edit.html', PasswordForm=PasswordForm)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    UsernameForm = EditUsernameForm()
    PictureForm = ChangeProfilePicture()
    NameForm = EditNameForm()
    PasswordForm = ChangePasswordForm()
    EmailForm = ChangeEmailForm()

    if PictureForm.validate_on_submit():
        if PictureForm.profile_img.data:
            print("In Pictore Submitted")
            picture_file = save_picture(PictureForm.profile_img.data, 0)
            current_user.profile_img = picture_file
            print(picture_file)
            db.session.commit()
    elif UsernameForm.validate_on_submit():
        print("Change Name")
        current_user.username = UsernameForm.username.data
        db.session.commit()
        flash('Your changes have been saved.')
    elif NameForm.validate_on_submit():
        print(NameForm.firstName.data)
        print(NameForm.lastName.data)
        current_user.first_name = NameForm.firstName.data
        current_user.last_name = NameForm.lastName.data
        db.session.commit()
    elif PasswordForm.validate_on_submit():
        print("Password Form")
        if current_user.check_password(PasswordForm.currentPassword.data):
            current_user.set_password(PasswordForm.password)
            db.session.commit()
    elif EmailForm.validate_on_submit():
        current_user.email = EmailForm.email.data
        db.session.commit()
    elif request.method == 'GET':
        UsernameForm.username.data = current_user.username
        NameForm.firstName.data = current_user.first_name
        NameForm.lastName.data = current_user.last_name
        EmailForm.email.data = current_user.email

    return render_template('edit_profile.html', PasswordForm=PasswordForm, UsernameForm=UsernameForm, NameForm=NameForm,
                           EmailForm=EmailForm, user=current_user, PictureForm=PictureForm)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/events')
@login_required
def events():
    events = Event.query.order_by(Event.timestamp.desc())
    return render_template('events.html', events=events)


@app.route('/documents')
def documents():
    return render_template('documents.html')


@app.route("/get_pdf/<filename>")
def get_pdf(filename):
    print(filename)
    try:
        return send_from_directory(app.config["CLIENT_PDF"], filename=filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)


@app.route('/maintenance', methods=['GET', 'POST'])
@login_required
def maintenance():
    maintenance_post = Maintenance.query.order_by(Maintenance.date.desc())
    return render_template('maintenance.html', maintenance_post=maintenance_post)


@app.route('/maintenance_form', methods=['GET', 'POST'])
@login_required
def maintenance_form():
    form = MaintenanceForm()

    if form.validate_on_submit():
        picture_file = None
        if form.img.data:
            picture_file = save_picture(form.img.data, 3)
        post = Maintenance(title=form.title.data, body=form.body.data, start=form.start_at.data, end=form.end_at.data,
                           date=form.date.data, author=current_user, maintenance_img=picture_file)
        db.session.add(post)
        db.session.commit()
        send_maintenance_post(User.query.all(), post)
        flash('Maintenance Form Successful')
        return redirect(url_for('home'))
    return render_template('maintenance_form.html', title='Maintenance Report', form=form)


@app.route('/event_form', methods=['GET', 'POST'])
@login_required
def event_form():
    form = EventForm()
    if form.validate_on_submit():
        picture_file = None
        if form.img.data:
            picture_file = save_picture(form.post_img.data, 2)
        event = Event(title=form.title.data, body=form.body.data, dateOfEvent=form.dateOfEvent.data,
                      start=form.start_at.data, end=form.end_at.data, img=picture_file)
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
            return render_template('login.html', error=error, form=form)
        elif not user.check_password(form.password.data):
            error = 'Wrong password. Try again or click Forgot password to reset it'
            return render_template('login.html', error=error, form=form)
        else:
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('home'))
    return render_template('login.html', form=form)


@app.route('/registration_request', methods=['GET', 'POST'])
def registration_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    email = 'nikocolon94@gmail.com'
    send_user_registeration_email(email)
    flash('Check your email for the instructions to register as a user')
    return redirect(url_for('login'))


def save_picture(form_picture, type):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext

    if type == 0:
        picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    elif type == 1:
        picture_path = os.path.join(app.root_path, 'static/post_pic', picture_fn)
    elif type == 2:
        picture_path = os.path.join(app.root_path, 'static/event_pic', picture_fn)
    elif type == 3:
        picture_path = os.path.join(app.root_path, 'static/maintenance_pic', picture_fn)

    form_picture.save(picture_path)
    return picture_fn


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        if form.profile_pic.data:
            picture_file = save_picture(form.profile_pic.data)
            print(picture_file)
        user = User(username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data,
                    phone_number=form.phone.data, email=form.email.data, profile_img=picture_file,
                    email_notification=form.email_notification.data, test_notification=form.mobile_notification.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    else:
        print(form.errors)

    return render_template('register.html', form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        recipent = form.email.data

        if user:
            send_password_reset_email(user, recipent)
        else:
            send_unknow_user_email(recipent)

        return render_template('reset_password_confirmation.html', email=recipent)
    return render_template('reset_password_request.html', title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('reset_password_link_expired'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        send_password_change_confirmation(user, user.email)
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
