import os

from flask import render_template, redirect, request, session, flash
from flask_app import app


from flask_app.models.musicians_model import Musician
from flask_app.models.users_model import User



# TODO -------- change this to route to dashboard -------
@app.route("/")
@app.route("/dashboard")
def index():
    # print( os.environ.get("CLIENT_ID") )
    # print( os.environ.get("CLIENT_SECRET") )
    # print( os.environ.get("REDIRECT_URI") )




    if "user_id" not in session:
        flash("Must login to see this page.")
        return redirect("/login/users")



    musicians = Musician.get_all()

    return render_template("dashboard.html", musicians = musicians)





@app.route("/register/users")
def register():
    return render_template("user_registration.html")




@app.route("/register_user", methods=["POST"])
def register_user():

    if not User.validate_new(request.form):
        return redirect("/register/users")
    
    session["user_id"] = User.create(request.form)

    return redirect("/")



@app.route("/login/users")
def show_user_login():
    return render_template("user_login.html")


@app.route("/login_user", methods=["POST"])
def login_user():

    logged_in_user = User.validate_login(request.form)

    if not logged_in_user:
        return redirect("/login/users")
    
    session["user_id"] = logged_in_user.id


    return redirect("/")





@app.route("/logout_user")
def logout_user():
    session.pop("user_id", None)
    return redirect("/login/users")





@app.route("/users/my_profile")
def my_profile():

    if "user_id" not in session:
        flash("Must login to see this page.")
        return redirect("/login/users")

    user = User.get_one_by_id({"id":session["user_id"]})

    print(user.gigs)
    return render_template("my_profile.html", user = user)










@app.route("/spotify")
def spotify_test():
    return "hello there"