from re import template
from flask_app import app
from flask import flash, redirect, render_template, request, session
from flask_app.models.user import User
from flask_app.models.vehicle import Vehicle

app.config['STRIPE_PUBLIC_KEY'] = ''
app.config['STRIPE_SECRET_KEY'] = ''


@app.route("/start_renew")
def reg_renew_page():
    return render_template("reg_renew.html")


@app.route('/find_vehicle', methods=['post'])
def find_vehicle():
    data = {
        'plate': request.form['plate'],
        'right(vin,5)': request.form['VIN']
    }
    # print(data['plate'])
    # print(data['VIN'])
    vehicle_in_db = Vehicle.get_vehicle_by_plate(data)
    print(data['plate'])
    print(data['right(vin,5)'])
    print(vehicle_in_db)
    if not vehicle_in_db:
        print(f'trying to find plate')
        flash('Invalid Plate Number')
        return redirect("/start_renew")

    session['vehicle_id'] = vehicle_in_db[0]['id']
    return redirect("/reg_renew_vehicle")


@app.route("/reg_renew_vehicle")
def reg_vehicle():
    if "vehicle_id" not in session:
        return redirect("/start_renew")
    data = {
        "id": session["vehicle_id"]
    }
    vehicle_in_db = Vehicle.get_vehicle_by_id(data)
    return render_template("/renew_vehicle.html", vehicle=vehicle_in_db)


@app.route("/reg_payment")
def reg_payment_page():
    if "vehicle_id" not in session:
        return redirect("/start_renew")
    else:
        return render_template("reg_renew_payment.html")


@app.route("/complete_renew")
def complete_renew_page():
    if "vehicle_id" not in session:
        return redirect("/start_renew")
    data = {
        "id": session ["vehicle_id"]
    }
    vehicle_in_db = Vehicle.get_vehicle_by_id(data)
    return render_template ("/complete_renew.html", vehicle = vehicle_in_db)