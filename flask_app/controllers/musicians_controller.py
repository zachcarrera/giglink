import os

from flask import render_template, redirect, request, session, flash
from flask_app import app

from flask_app.models.musicians_model import Musician



import spotipy
from spotipy.oauth2 import SpotifyClientCredentials



CLIENT_ID =  os.environ.get("CLIENT_ID")
CLIENT_SECRET =  os.environ.get("CLIENT_SECRET")



@app.route("/register/musicians")
def show_musician_register():
    return render_template("musician_registration.html")


@app.route("/register_musician", methods=["POST"])
def register_musician():
    print(request.form)

    if not Musician.validate_new(request.form):
        return redirect("/register/musicians")

    
    session["musician_id"] = Musician.create(request.form)

    return redirect("/musician/my_gigs")





# route to show musician login page
@app.route("/login/musicians")
def show_musician_login():
    return render_template("musician_login.html")


@app.route("/login_musician", methods=["POST"])
def login_musician():

    logged_in_musician = Musician.validate_login(request.form)

    if not logged_in_musician:
        return redirect("/login/musicians")
    
    session["musician_id"] = logged_in_musician.id
    return redirect("/musician/my_gigs")





@app.route("/logout_musician")
def logout_musician():
    session.pop("musician_id", None)
    return redirect("/login/musicians")















@app.route("/update_musician", methods=["POST"])
def update_musician():

    print(request.form)

    Musician.update(request.form)

    return redirect("/musician/my_gigs")

















# route to show results of a given search query
@app.route("/search")
def search():


    if "user_id" not in session:
        flash("Must login to see this page.")
        return redirect("/login/users")
    

    # todo call class to run query to find matches

    search_query = request.args.get("search")

    results = Musician.search_by_stage_name({"stage_name": search_query})

    return render_template("search_results.html", search_query = search_query, results = results)



@app.route("/musician/profile/<int:musician_id>")
def show_musician(musician_id):


    if "user_id" not in session:
        flash("Must login to see this page.")
        return redirect("/login/users")


    musician = Musician.get_one_by_id({"id": musician_id})

    artist_id = get_artist_id(musician.stage_name)

    return render_template("musician_profile.html", musician = musician, artist_id = artist_id)


@app.route("/musician/my_gigs")
def my_gigs():


    # Todo ----- check session for id and either redirect
    # or query data

    if "musician_id" not in session:
        flash("Must log in to a musician account to view page")
        return redirect("/login/musicians")

    musician = Musician.get_one_by_id({"id" : session["musician_id"]})


    return render_template("my_gigs.html", musician = musician)




def get_spotify_client_cred():
    return SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)



def get_artist_id(artist_name):
    auth_manager = get_spotify_client_cred()
    sp = spotipy.Spotify(auth_manager = auth_manager)

    results = sp.search(artist_name, type = "artist")

    if not results["artists"]["items"]:
        return False


    artist_id = results["artists"]["items"][0]["id"]
    return artist_id
