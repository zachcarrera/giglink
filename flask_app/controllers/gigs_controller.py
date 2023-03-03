from flask import render_template, redirect, request, session, flash
from flask_app import app

from flask_app.models.gigs_model import Gig

@app.route("/new_gig", methods = ["POST"])
def new_gig():


    print(request.form)

    Gig.create(request.form)


    flash(f"Booking for {request.form['gig_at']} successful!")

    return redirect(f"/musician/profile/{request.form['musician_id']}")