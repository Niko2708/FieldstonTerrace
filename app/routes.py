from flask import render_template, flash, redirect, url_for, request, send_file, send_from_directory, safe_join, abort
from app import app, db
from app.forms import *
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Maintenance, Event, CommunityBoard
from app.email import *
from app.forms import ResetPasswordForm

# routes for resident users that login in
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    image_file = url_for('static', filename='profile_pics/default.jpg')
    form = CommunityBoardForm()
    if form.validate_on_submit():
        posts = CommunityBoard(title=form.title.data, body=form.post.data, post_img=form.post_img.data, author=current_user)
        db.session.add(posts)
        db.session.commit()
        flash('Post Successful')
    posts = CommunityBoard.query.order_by(CommunityBoard.timestamp.desc()).all()
    maintenance_post = Maintenance.query.order_by(Maintenance.timestamp.desc()).all()
    return render_template('home.html', form=form, posts=posts,maintenance_post=maintenance_post, image_file=image_file)

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
        post.body = form.body.data
        post.post_img = form.post_img.data
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
    image_file = url_for('static', filename='profile_pics/default.jpg')
    user = User.query.filter_by(username=username).first_or_404()
    posts = CommunityBoard.query.order_by(CommunityBoard.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts, image_file=image_file)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    UsernameForm = EditUsernameForm()
    NameForm = EditNameForm()
    PasswordForm = ChangePasswordForm()

    if UsernameForm.validate_on_submit():
        current_user.username = UsernameForm.username.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif NameForm.validate_on_submit():
        current_user.firstName = NameForm.firstName.data
        current_user.lastName = NameForm.lastName.data
        db.session.commit()
        return redirect(url_for('edit_profile'))
    elif PasswordForm.validate_on_submit():
        if current_user.check_password(PasswordForm.currentPassword.data):
            current_user.set_password(PasswordForm.password)
            db.session.commit()
    elif request.method == 'GET':
        UsernameForm.username.data = current_user.username
        NameForm.firstName.data = current_user.first_name
        NameForm.lastName.data = current_user.last_name

    return render_template('edit_profile.html', PasswordForm=PasswordForm, UsernameForm=UsernameForm, NameForm=NameForm,
                           user=current_user)


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
        post = Maintenance(title=form.title.data, body=form.body.data, start=form.start_at.data, end=form.end_at.data,
                           date=form.date.data, author=current_user)
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
        event = Event(title=form.title.data, body=form.body.data, dateOfEvent=form.dateOfEvent.data,
                      start=form.start_at.data, end=form.end_at.data)
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


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, first_name=form.first_name.data, last_name = form.last_name.data,
                    phone_number = form.phone.data, email=form.email.data, profile_img=form.profile_pic.data,
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
