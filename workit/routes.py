from flask import render_template, request, redirect, session, url_for, flash
from workit.forms import SearchForm, LoginForm, SignupForm, EditProfileForm
from workit import app, offers_collection, users_collection
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
        offers = offers_collection.find(query)
        return render_template(
                "layout.html",
                offers=offers,
                searchForm=searchForm,
                loginForm=loginForm,
                signupForm=signupForm
            )
    else:
        if offers_collection.count_documents({}) == 0:
            for website in WEBSITES:
                website.create_offers()
                offers_collection.insert_many(
                    [dict(offer) for offer in website.offers]
                )
        return render_template(
            "layout.html",
            offers=offers_collection.aggregate([{"$sample": {"size": 20}}]),
            searchForm=searchForm,
            loginForm=loginForm,
            signupForm=signupForm
        )

# Test for non-logged users
@app.route('/profile/<name>', methods=['GET'])
@login_required
def profile(name):
    user = current_user.name
    editProfileForm = EditProfileForm()
    return render_template(
        'profile.html',
        user=user,
        current_user=current_user,
        editProfileForm=editProfileForm,
        body="You are now logged in!"
    )


# holer was made for tests. Looking for a proper way for change data on site
@app.route('/profile/<name>/edit/<holder>', methods=['GET', 'POST']) #holder
@login_required
def editProfile(name, holder): #holder
    editProfileForm = EditProfileForm()
    user = current_user.name
    if request.method == 'POST':
        payload = {"$set": {}}
        if editProfileForm.name.data:
            holder = editProfile.name.data # holer
            payload["$set"] = {"name": editProfileForm.name.data}
        if editProfileForm.github.data:
            holder = editProfile.github.data # holder
            payload["$set"] = {"github": editProfileForm.github.data}
        users_collection.update_one({"_id": current_user.get_id()}, payload)
        flash('Your change have been saved.')
        return redirect(url_for('profile', name=name))

    return render_template(
        'editProfile.html',
        title='Edit Profile',
        user=user,
        holder=holder, #holder
        current_user=current_user,
        editProfileForm=editProfileForm
    )


@app.route("/logout")
@login_required
def logout():
    session['logged_in'] = False
    logout_user()
    return redirect(url_for('.home'))
