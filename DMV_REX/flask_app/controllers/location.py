from flask_app import app
from flask import flash, redirect, render_template, request, session
from flask_app.models.user import User


@app.route("/aaa_location")
def aaa_page():
    return render_template ("AAA_locations.html")

@app.route("/kiosk_location")
def kiosk_page():
    return render_template ("kiosk_locations.html")