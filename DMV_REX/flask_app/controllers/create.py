from flask_app import app
from flask import flash, redirect, render_template, request, session

from flask_app.models.user import User

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/user_signup")
def new_account():
    return render_template ("sign-up.html")

@app.route('/signup', methods = ['post'])
def signup():
    #check the flash validation
    if not User.validate_user(request.form):
        return redirect('/user_signup')
    #check if email already in use
    data = {
        'email' : request.form ['email']
    }
    user_in_db = User.get_user_by_email(data)
    
    if user_in_db: 
        flash ('Email is already taken')
        return redirect('/user_signup')
    else:
    #register user
    # create the hash
        pw_hash = bcrypt.generate_password_hash(request.form["password"])
        data = {
            "first_name": request.form ["first_name"],
            "last_name": request.form ["last_name"],
            "email": request.form ["email"],
            # put the pw_hash into the data dictionary
            "password": pw_hash
        }
        # Call the save @classmethod on User
        user_id = User.register_user(data)
        session['user_id'] = user_id
        return redirect('/user_page')

@app.route ("/user_signin")
def signin():
    return render_template ("sign-in.html")


@app.route('/signin', methods = ['post'])
def login():
    # see if the username provided exists in the database
    data = {
        'email' : request.form ['email']
    }
    user_in_db = User.get_user_by_email(data)
    # if user is not registered in the db
    if not user_in_db:
        flash ('Invalid Email/Password')
        return redirect ("/user_signin")
    # if we get False after checking the password (email is valid)
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash ('Invalid Email/Password')
        return redirect ("/user_signin")
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    return redirect ('/user_page')


@app.route("/user_logout")
def user_logout():
    if "user_id" in session:
        del session["user_id"]
    return redirect(request.referrer)