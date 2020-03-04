from flask import Blueprint, redirect, render_template, flash, request, session, url_for
from flask_login import login_required, logout_user, current_user, login_user
from workit.forms import LoginForm, SignupForm
from workit.model.User import User
from workit import login_manager, client, app


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('.dashboard'))
    
    login_form = LoginForm()

    if request.method == 'POST':
        # OBECNIE DANE WPROWADZONE NA SZTYWNO------------
        # if request.form['email'] != 'admin@admin.pl' or request.form['password'] != 'admin1':
        #     flash('Invalid username or password')
        # else:
        #     return redirect(url_for('.home'))
        # BRAK POLACZENIA Z BAZA------------------------
        if login_form.validate_on_submit():
            email = login_form.get('email')
            password = login_form.get('password')
            user = User.query.filter_by(email=email.first())
            
            if user and user.check_password(password=password):
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page or url_for('.dashboard'))
            
            flash('Invalid username or password')
            return redirect(url_for('.login'))

    return render_template('login.html',
                            title='Log in.',
                            form=login_form,
                            template='login-page',
                            body="Log in with your User account.")

@app.route('/signup', methods=['GET', 'POST'])
def signup():

    signup_form = SignupForm()
    if request.method == 'POST':
        if signup_form.validate_on_submit():
            name = signup_form.get('name')
            email = signup_form.get('email')
            password = signup_form.get('password')
            github = signup_form.get('github')
            existing_user = User.query.filter_by(email=email).first()
            if existing_user is None:
                user = User(name=name,
                            email=email,
                            github=github)
                user.set_password(password)
                client.db.session.add(user)
                client.db.session.commit()
                login_user(user)
                return redirect(url_for('.dashboard'), code=400)
            flash('A user already exists with that email address.')
            return redirect(url_for('.signup'))

    return render_template('signup.html',
                        title='Create an Account.',
                        form=signup_form,
                        template='signup-page',
                        body="Sign up for a user account.")

@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None

@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to view that page.')
    return redirect(url_for('.login'))