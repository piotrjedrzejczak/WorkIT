from flask import redirect, render_template, flash, request, url_for
from flask_login import current_user, login_user
from workit.forms import LoginForm, SignupForm
from workit.model.User import User
from workit import login_manager, app


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('.home'))
    login_form = LoginForm()
    if request.method == 'POST':
        if login_form.validate_on_submit():
            email = login_form.email.data
            password = login_form.password.data
            user = User.get_by_email(email)
            if user and user.check_password(password=password):
                login_user(user)
                return redirect(url_for('.home'))
            flash('Invalid username or password')
            return redirect(url_for('.login'))

    return render_template(
        'login.html',
        title='Log in.',
        form=login_form,
        template='login-page',
        body="Log in with your User account."
    )


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = SignupForm()
    if request.method == 'POST':
        if signup_form.validate_on_submit():
            flash('Wyjebalem sie 111111')
            name = signup_form.name.data
            email = signup_form.email.data
            password = signup_form.password.data
            existing_user = User.get_by_email(email)
            flash('Wyjebalem sie')
            if existing_user is None:
                user = User(
                    name=name,
                    email=email,
                    password=password
                )
                user.save_user()
                login_user(user)
                return redirect(url_for('.home'))
            flash('A user already exists with that email address.')
            return redirect(url_for('.signup'))

    return render_template(
        'signup.html',
        title='Create an Account.',
        form=signup_form,
        template='signup-page',
        body="Sign up for a user account."
    )


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.get_by_id(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to view that page.')
    return redirect(url_for('.login'))
