from flask import render_template, flash, redirect, url_for, request, send_file, send_from_directory, safe_join, abort
from app import app, db
from app.forms import *
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Maintenance, Event, CommunityBoard
from app.email import *
from app.text import send_maintenance_text
import os
import secrets


# routes for resident users that login in
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    posts = CommunityBoard.query.order_by(CommunityBoard.timestamp.desc()).all()
    maintenance_posts = Maintenance.query.order_by(Maintenance.timestamp.desc()).limit(2).all()

    return render_template('home.html', posts=posts, maintenance_posts=maintenance_posts)

@app.route('/post_form', methods=['GET', 'POST'])
@login_required
def post_form():
    form = CommunityBoardForm()
    if form.validate_on_submit():
        picture_file = None
        if form.post_img.data:
            picture_file = save_picture(form.post_img.data, 1)

        posts = CommunityBoard(title=form.title.data, body=form.post.data, post_img=picture_file, author=current_user)
        db.session.add(posts)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_post.html', title='Post', form=form, legend='Post')


@app.route("/maintenance/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_maintenance(post_id):
    post = Maintenance.query.get_or_404(post_id)

    dirname = os.path.dirname(__file__)
    path = dirname + '/static/maintenance_pic/' + str(post.maintenance_img)


    if post.author != current_user:
        abort(403)

    if os.path.exists(path):
        os.remove(path)

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
            if post.maintenance_img != None:
                dirname = os.path.dirname(__file__)
                path = dirname + '/static/maintenance_pic/' + str(post.maintenance_img)

                if os.path.exists(path):
                    os.remove(path)

            picture_file = save_picture(form.img.data, 3)
            post.maintenance_img = picture_file
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.body.data = post.body
    return render_template('maintenance_form.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = CommunityBoard.query.get_or_404(post_id)
    dirname = os.path.dirname(__file__)
    path = dirname + '/static/post_pic/' + str(post.post_img)

    if post.author != current_user:
        abort(403)

    if os.path.exists(path):
        os.remove(path)

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
            if post.post_img != None:
                dirname = os.path.dirname(__file__)
                path = dirname + '/static/post_pic/' + str(post.post_img)

                if os.path.exists(path):
                    os.remove(path)

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


@app.route("/event/<int:event_id>/delete", methods=['POST'])
@login_required
def delete_event(event_id):
    post = Event.query.get_or_404(event_id)
    dirname = os.path.dirname(__file__)
    path = dirname + '/static/event_pic/' + str(post.event_img)

    if post.author != current_user:
        abort(403)

    if os.path.exists(path):
        os.remove(path)

    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/event/<int:event_id>/update", methods=['GET', 'POST'])
@login_required
def event_update(event_id):
    post = Event.query.get_or_404(event_id)

    if post.author != current_user:
        abort(403)

    form = EventForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        if form.img.data:
            if post.event_img != None:
                dirname = os.path.dirname(__file__)
                path = dirname + '/static/event_pic/' + str(post.event_img)

                if os.path.exists(path):
                    os.remove(path)
            picture_file = save_picture(form.img.data, 2)
            post.event_img = picture_file
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('events'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.body.data = post.body
        form.img.data = post.event_img
    return render_template('event_form.html', title='Update Post',
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
        return redirect(url_for('edit_profile'))
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
        return redirect(url_for('edit_profile'))
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
            return redirect(url_for('edit_profile'))
        elif not current_user.check_password(PasswordForm.password.data):
            error = 'Wrong password'
            return render_template('editForm/password.html', error=error, PasswordForm=PasswordForm)

    return render_template('editForm/password_edit.html', PasswordForm=PasswordForm)


@app.route('/edit_profile/change_photo', methods=['GET', 'POST'])
@login_required
def change_photo():
    form = ChangeProfilePicture()
    if form.validate_on_submit():
        if form.profile_img.data:
            if current_user.profile_img != None:
                dirname = os.path.dirname(__file__)
                path = dirname + '/static/profile_pic/' + str(current_user.profile_img)

                if os.path.exists(path) and current_user.profile_img != 'default.jpeg':
                    os.remove(path)

            picture_file = save_picture(form.profile_img.data, 0)
            current_user.profile_img = picture_file
            db.session.commit()
        return redirect(url_for('edit_profile'))
    return render_template('editForm/photo.html', form=form)


@app.route('/edit_profile/change_name', methods=['GET', 'POST'])
@login_required
def change_name():
    form = EditNameForm()
    if form.validate_on_submit():
        current_user.first_name = form.firstName.data
        current_user.last_name = form.lastName.data
        db.session.commit()
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.firstName.data = current_user.first_name
        form.lastName.data = current_user.last_name

    return render_template('editForm/name_edit.html', form=form)


@app.route('/edit_profile/username', methods=['GET', 'POST'])
@login_required
def change_username():
    form = EditUsernameForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username

    return render_template('editForm/username_edit.html', form=form)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = current_user
    return render_template('edit_profile.html', user=user)


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
    maintenance_post = Maintenance.query.order_by(Maintenance.timestamp.desc())
    return render_template('maintenance.html', maintenance_post=maintenance_post)

@app.route('/maintenance_form', methods=['GET', 'POST'])
@login_required
def maintenance_form():
    form = MaintenanceForm()

    if form.validate_on_submit():
        picture_file = None
        if form.img.data:
            picture_file = save_picture(form.img.data, 3)
        post = Maintenance(title=form.title.data, body=form.body.data,author=current_user, maintenance_img=picture_file)
        db.session.add(post)
        db.session.commit()
        send_maintenance_email(User.query.all(), post)
        send_maintenance_text(User.query.all(), post)
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
            picture_file = save_picture(form.img.data, 2)

        event = Event(title=form.title.data, body=form.body.data, author=current_user, event_img=picture_file)
        db.session.add(event)
        db.session.commit()
        flash('Maintenance Form Successful')
        return redirect(url_for('events'))
    return render_template('event_form.html', form=form)


# routes for non resident users
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/amenities')
def amenities():
    return render_template('amenities.html')


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
        return redirect(url_for('login'))

    form = RegistrationForm()

    if form.validate_on_submit():
        picture_file = 'default.jpeg'

        if form.profile_pic.data:
            picture_file = save_picture(form.profile_pic.data,0)

        user = User(username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data,
                    phone_number=form.phone.data, email=form.email.data, profile_img=picture_file,
                    email_notification=form.email_notification.data, text_notification=form.mobile_notification.data)
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
        user = User.query.filter_by( form.email.data).first()
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
