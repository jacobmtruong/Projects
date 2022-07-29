from flask_app import app
from flask import flash, redirect, render_template, request, session
from flask_app.models.user import User

# from flask_app.models.owner import Owner


@app.route("/")
def main_page():
    if "vehicle_id" not in session:
        del session ['vehicle_id']
    return render_template("main_page.html")


@app.route("/renew")
def renew_prep():
    return render_template("renew_prep.html")

#display user in session personal infomation on user_page
@app.route("/user_page")
def user_page():
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": session ["user_id"]
    }
    user_in_db = User.get_user_by_id(data)
    return render_template ("/user_page.html", user = user_in_db)
    

@app.route("/edit_page/<int:id>")
def edit_user_page(id):
    user = User.get_user_by_id({"id":id})
    return render_template ("edit_user.html",user=user)


@app.route('/user_editted/<int:id>', methods = ['post'])
def edit_submit(id):
    if "user_id" not in session:
        return redirect("/")

    if not User.validate_address(request.form):
        #can not take in <int:id>, it has to be str(id)
        return redirect('/edit_page/'+ str(id)) 

    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email" : request.form["email"],
        "id_card" : request.form["id_card"],
        "address" : request.form["address"],
        "city" : request.form["city"],
        "state" : request.form["state"],
        "zip_code" : request.form["zip_code"],
        "id" : id
    }
    User.edit_user(data)
    return redirect ('/user_page')


