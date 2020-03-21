from flask import redirect, render_template, flash, request, url_for, session
from flask_login import login_user
from workit.forms import LoginForm, SignupForm, SearchForm
from workit.model.User import User
from workit import login_manager, app


@app.route('/login', methods=['POST'])
def login():
    searchForm = SearchForm()
    loginForm = LoginForm()
    # if current_user.is_authenticated:
    #     return redirect(url_for('.home'))
    if request.method == 'POST':
        if loginForm.validate_on_submit():
            email = loginForm.email.data
            password = loginForm.password.data
            user = User.get_by_email(email)
            if user and user.check_password(password=password):
                login_user(user)
                session['logged_in'] = True
                return redirect(url_for('home'))
            flash('Invalid username or password')
            return redirect(url_for('home'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signupForm = SignupForm()
    if request.method == 'POST':
        if signupForm.validate_on_submit():
            name = signupForm.name.data
            email = signupForm.email.data
            password = signupForm.password.data
            existing_user = User.get_by_email(email)
            if existing_user is None:
                user = User(
                    name=name,
                    email=email,
                    password=password
                )
                user.set_password(password)
                user.save_user()
                login_user(user)
                return redirect(url_for('.home'))
            flash('A user already exists with that email address.')
            return redirect(url_for('.signup'))

    return render_template(
        'signup.html',
        title='Create an Account.',
        signupForm=signupForm,
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
