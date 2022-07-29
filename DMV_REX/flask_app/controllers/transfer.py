from flask_app import app
from flask import flash, redirect, render_template, request, session
from werkzeug.utils import secure_filename
import os
from flask_app.models.user import User
from flask_app.models.vehicle import Vehicle


@app.route("/transfer")
def transfer_prep_page():
    return render_template("transfer_prep.html")


@app.route("/get_vehicle_info_transfer")
def get_vehicle__info_transfer():
    return render_template("transfer_get_vehicle.html")


@app.route('/find_vehicle_for_transfer', methods=['post'])
def find_vehicle_for_transfer():
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
        return redirect("/get_vehicle_info_transfer")

    session['vehicle_id'] = vehicle_in_db[0]['id']
    return redirect("/transfer_vehicle")


@app.route("/transfer_vehicle")
def transfer_vehicle():
    if "vehicle_id" not in session:
        return redirect("/get_vehicle_info_transfer")
    data = {
        "id": session["vehicle_id"]
    }
    vehicle_in_db = Vehicle.get_vehicle_by_id(data)
    return render_template("transfer_step_one.html", vehicle=vehicle_in_db)


@app.route("/transfer_vehicle_new_owner/<int:id>", methods=["post"])
def transfer_vehicle_new_owner(id):
    if not Vehicle.validate_new_owner(request.form):
        return redirect("/transfer_vehicle")

    else:

        data = {
            "owner_first_name": request.form["owner_first_name"],
            "owner_last_name": request.form["owner_last_name"],
            "owner_id_card": request.form["owner_id_card"],
            "address": request.form["address"],
            "city": request.form["city"],
            "state": request.form["state"],
            "zip_code": request.form["zip_code"],
            "id": id
        }
        Vehicle.update_vehicle_with_new_owner(data)
        return redirect("/transfer_step_two")


@app.route("/transfer_step_two")
def transfer_step_two():
    if "vehicle_id" not in session:
        return redirect("/start_renew")
    data = {
        "id": session["vehicle_id"]
    }
    vehicle_in_db = Vehicle.get_vehicle_by_id(data)
    return render_template("transfer_step_two.html", vehicle=vehicle_in_db)


@app.route('/upload', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    return redirect("/transfer_step_two")


@app.route('/transfer_step_three')
def transfer_step_three_page():
    return render_template ("transfer_step_three.html")

@app.route('/complete_transfer')
def complete_transfer():
    return render_template ("complete_transfer.html")