from flask import render_template, request, redirect, session, url_for
from workit.forms import SearchForm, LoginForm, SignupForm
from workit import app, collection
from workit.const import WEBSITES
from flask_login import current_user, login_required, logout_user


@app.route('/', methods=['GET', 'POST'])
def home():
    searchForm = SearchForm()
    loginForm = LoginForm()
    signupForm = SignupForm()
    if request.method == 'POST':
        query = {}
        if searchForm.keyword.data:
            query.update({"$text": {"$search": searchForm.keyword.data}})
        if searchForm.categories.data:
            query.update({"category": searchForm.categories.data})
        if searchForm.cities.data:
            query.update({"city": searchForm.cities.data})
        offers = collection.find(query)
        return render_template(
                "layout.html",
                offers=offers,
                searchForm=searchForm,
                loginForm=loginForm,
                signupForm=signupForm
            )
    else:
        if collection.count_documents({}) == 0:
            for website in WEBSITES:
                website.create_offers()
                collection.insert_many(
                    [dict(offer) for offer in website.offers]
                )
        return render_template(
            "layout.html",
            offers=collection.aggregate([{"$sample": {"size": 20}}]),
            searchForm=searchForm,
            loginForm=loginForm,
            signupForm=signupForm
        )

# Test for non-logged users
@app.route('/profile', methods=['GET'])
@login_required
def profile():
    searchForm = SearchForm()

    return render_template(
        'profile.html',
        searchForm=searchForm,
        title='Flask-Login',
        current_user=current_user,
        body="You are now logged in!"
    )

# TODO: logout implementation
@app.route("/logout")
@login_required
def logout():
    session['logged_in'] = False
    logout_user()
    return redirect(url_for('.home'))