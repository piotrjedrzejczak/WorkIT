from flask import redirect, render_template, flash, request, url_for
from flask_login import login_user, logout_user, current_user, login_required
from workit import login_manager, app
from workit.model.User import User
from workit.model.Newsletter import Newsletter
from workit.forms import (
    LoginForm,
    SignupForm,
    ChangePasswordForm,
    ChangeGithubURLForm,
    ChangeEmailForm,
    ChangeNameForm,
    NewsletterForm
)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        flash('You are already logged in', category='info')
        return redirect(url_for('.home'))
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            user = User.get_by_email(email)
            if user and user.verify_password(password):
                login_user(user)
                return redirect(url_for('home'))
            flash('Invalid Username or Password.', category='danger')
        return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            existing_user = User.get_by_email(form.email.data)
            if not existing_user:
                user = User(
                    name=form.name.data,
                    email=form.email.data,
                    github=form.github.data
                )
                user.password = form.password.data
                user.save_user()
                login_user(user)
                flash('Account Created Sucessfully', category='success')
                return redirect(url_for('.home'))
            flash('User already exists with that email address.', category='danger')
            return redirect(url_for('.signup'))
        return render_template('signup.html', form=form)
    return render_template('signup.html', form=form)


@app.route("/profile", methods=["GET"])
@login_required
def profile():
    return render_template("profile.html")


@app.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if current_user.verify_password(form.old_password.data):
                current_user.password = form.new_password.data
                current_user.update_field('password_hash', current_user.password_hash)
                flash('Your Password Has Been Updated', category='success')
                return redirect(url_for('profile'))
            else:
                flash('Wrong Password', category='danger')
        return render_template('changepasswordform.html', form=form)
    return render_template('changepasswordform.html', form=form)


@app.route("/change-name", methods=["GET", "POST"])
@login_required
def change_name():
    form = ChangeNameForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            current_user.update_field('name', form.new_name.data)
            flash('Your Username Has Been Updated', category='success')
            return redirect(url_for('profile'))
        return render_template('changenameform.html', form=form)
    return render_template('changenameform.html', form=form)


@app.route("/change-github", methods=["GET", "POST"])
@login_required
def change_github():
    form = ChangeGithubURLForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            current_user.update_field('github', form.new_github_url.data)
            flash('Your Github URL Has Been Updated', category='success')
            return redirect(url_for('profile'))
        return render_template('changegithubform.html', form=form)
    return render_template('changegithubform.html', form=form)


@app.route("/change-email", methods=["GET", "POST"])
@login_required
def change_email():
    form = ChangeEmailForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if not User.get_by_email(form.new_email.data):
                current_user.update_field('email', form.new_email.data)
                flash('Your Email Address Has Been Updated', category='success')
                return redirect(url_for('profile'))
            else:
                flash('Sorry, this email address is already taken.', category='danger')
        return render_template('changeemailform.html', form=form)
    return render_template('changeemailform.html', form=form)


@app.route("/configure-newsletter", methods=["GET", "POST"])
@login_required
def configure_newsletter():
    form = NewsletterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                newsletter = Newsletter(
                    current_user._id,
                    form.locations.data,
                    form.categories.data,
                    form.keywords.data,
                    form.max_results.data,
                    form.frequency.data
                )
                newsletter.timestamp()
                newsletter.save()
                flash('Your Newsletter Have Been Saved!', category='success')
                return redirect(url_for('profile'))
            except ValueError:
                flash('Invalid User', category='danger')
                return render_template('newsletterform.html', form=form)
        return render_template('newsletterform.html', form=form)
    return render_template('newsletterform.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out', category='info')
    return redirect(url_for(".home"))


@login_manager.user_loader
def load_user(id):
    if id is not None:
        return User.get_by_id(id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to view that page.')
    return redirect(url_for('.login'))
