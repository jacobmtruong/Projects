from crypt import methods
from xml.dom.minidom import Identified
from flask_app import app
from flask import flash, redirect, render_template, request, session
from flask_app.models.user import User

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# from flask_app.models.owner import Owner


@app.route("/")
def main_page():
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


@app.route('/change_pw_page/<int:id>')
def change_pw_page(id):
    user = User.get_user_by_id({'id':id})
    return render_template ("change_password.html", user = user)

@app.route('/update_new_password/<int:id>', methods = ['post'])
def update_new_password(id):
    if "user_id" not in session:
        return redirect ("/")
    
    pw_data = {
        "new_password":request.form ['new_password'],
        'confirm_new_password': request.form ['confirm_new_password']
    }
    if not User.validate_new_password(pw_data):
        return redirect ("/change_pw_page/" + str(id))

    user_in_db = User.get_user_by_id ({"id": session["user_id"]})
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash ("Invalid old password. Try again.")
        return redirect ( "/change_pw_page/" + str(id))
    
    if request.form['password'] == request.form['new_password']:
        flash ("New password cannot be the same as old password.")
        return redirect ( "/change_pw_page/" + str(id))

        # "/change_pw_page/" + str(id)

    pw_hash = bcrypt.generate_password_hash(request.form["new_password"])
    data = {
        "id": session ['user_id'],
        "new_password" : pw_hash
    }
    
    User.update_user_password(data)
    flash ("New Password Updated!")

    return redirect ("/user_page")