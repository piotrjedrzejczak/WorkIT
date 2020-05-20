from flask import render_template, request
from workit.forms import SearchForm
from workit import app, mongo


@app.route("/", methods=["GET", "POST"])
def home():
    searchForm = SearchForm()
    if request.method == "POST":
        results = mongo.search_offers(
            keyword=searchForm.keyword.data,
            category=searchForm.categories.data,
            city=searchForm.cities.data,
        )
        return render_template("home.html", offers=results, searchForm=searchForm)
    return render_template("home.html", offers=mongo.offers_sample(20), searchForm=searchForm)
