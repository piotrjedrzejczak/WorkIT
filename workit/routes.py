from flask import render_template, request
from workit.forms import SearchForm
from workit import app, mongo
from workit.const import WEBSITES


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
    else:
        if mongo.offers.count_documents({}) == 0:
            for website in WEBSITES:
                website.create_offers()
                mongo.insert_multiple_offers(website.serialize_offers())
        return render_template(
            "home.html", offers=mongo.offers_sample(20), searchForm=searchForm,
        )
