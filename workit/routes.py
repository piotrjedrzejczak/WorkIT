from flask import render_template, request, redirect, url_for
from workit.forms import SearchForm
from workit import app, collection
from workit.const import WEBSITES
from flask_login import current_user, login_required, logout_user


@app.route('/', methods=['GET', 'POST'])
def home():
    form = SearchForm()
    if request.method == 'POST':
        query = {}
        if form.keyword.data:
            query.update({"$text": {"$search": form.keyword.data}})
        if form.categories.data:
            query.update({"category": form.categories.data})
        if form.cities.data:
            query.update({"city": form.cities.data})
        offers = collection.find(query)
        return render_template(
                "layout.html",
                offers=offers,
                form=form
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
            form=form
        )

# Test for non-logged users
# @app.route('/home', methods=['GET'])
# @login_required
# def dashboard():
#     return render_template(
#         'layout.html',
#         title='Flask-Login',
#         current_user=current_user,
#         body="You are now logged in!"
#     )

# TODO: logout implementation
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))