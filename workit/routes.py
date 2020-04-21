from flask import render_template, request, redirect, session, url_for, flash
from workit.forms import SearchForm, EditProfileForm
from workit import app, mail, mongo
from workit.const import WEBSITES
from flask_login import current_user, login_required, logout_user
from flask_mail import Message


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


# Test for non-logged users
@app.route("/profile/<name>", methods=["GET"])
@login_required
def profile(name):
    user = current_user.name
    editProfileForm = EditProfileForm()
    return render_template(
        "profile.html",
        user=user,
        current_user=current_user,
        editProfileForm=editProfileForm,
        body="You are now logged in!",
    )


@app.route("/profile/<name>/editName", methods=["GET", "POST"])
@login_required
def editProfileName(name):
    editProfileForm = EditProfileForm()
    user = current_user.name
    if request.method == "POST":
        if editProfileForm.validate_on_submit():
            update_success = mongo.update_one_field(
                id=current_user.get_id(),
                field=name,
                value=editProfileForm.nameEdit.data,
            )
            if update_success:
                flash("Your change have been saved.")
            return redirect(url_for("profile", name=name))

    return render_template(
        "editProfileName.html",
        title="Edit Profile",
        user=user,
        current_user=current_user,
        editProfileForm=editProfileForm,
    )


@app.route("/profile/<name>/editGithub", methods=["GET", "POST"])
@login_required
def editProfileGithub(name):
    editProfileForm = EditProfileForm()
    user = current_user.name
    if request.method == "POST":
        if editProfileForm.validate_on_submit():
            update_success = mongo.update_one_field(
                id=current_user.get_id(),
                field="name",
                value=editProfileForm.nameEdit.data,
            )
            if update_success:
                flash("Your change have been saved.")
            return redirect(url_for("profile", name=name))

    return render_template(
        "editProfileGithub.html",
        title="Edit Profile",
        user=user,
        current_user=current_user,
        editProfileForm=editProfileForm,
    )


@app.route("/profile/<name>/editEmail", methods=["GET", "POST"])
@login_required
def editProfileEmail(name):
    editProfileForm = EditProfileForm()
    user = current_user.name
    if request.method == "POST":
        if editProfileForm.validate_on_submit():
            update_success = mongo.update_one_field(
                id=current_user.get_id(),
                field=name,
                value=editProfileForm.nameEdit.data,
            )
            if update_success:
                flash("Your change have been saved.")
            return redirect(url_for("profile", name=name))

    return render_template(
        "editProfileEmail.html",
        title="Edit Profile",
        user=user,
        current_user=current_user,
        editProfileForm=editProfileForm,
    )


@app.route("/profile/<name>/newsletter")
@login_required
def test_email(name):
    # body_template = render_template("test_email.txt", user=name)
    html_template = render_template("test_email.html", user=name)
    msg = Message(
        "Hello! %s" % current_user.name,
        sender="work.it@o2.pl",
        recipients=["m.luszczewski@o2.pl"],
    )
    # msg.body = body_template.encode('utf_8')
    msg.html = html_template.encode("utf_8")
    mail.send(msg)
    return "Sent"


@app.route("/logout")
@login_required
def logout():
    session["logged_in"] = False
    logout_user()
    return redirect(url_for(".home"))
