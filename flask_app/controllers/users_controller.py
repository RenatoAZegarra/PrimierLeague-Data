from flask import render_template, request, redirect, session
from flask_app import app
from flask import flash
from flask_app.models.user_model import User

@app.route( "/", methods=["GET"] )
def display_login_registration():
    return render_template( "index.html" )

@app.route( "/user/new", methods=["POST"] )
def create_user():
    if User.validate_user( request.form ) == False:
        return redirect( "/" )
    encrypted_password = User.encrypt_string( request.form["password"] )
    data = {
        **request.form,
        "password" : encrypted_password
    }
    user_id = User.create_one( data )
    session["user_id"] = user_id
    session["full_name"] = request.form["first_name"] + " " + request.form["last_name"]
    session["team_id"] = request.form["team_id"]
    return redirect( "/welcome" )

@app.route( "/login", methods=["POST"] )
def proccess_login():
    current_user = User.get_one( request.form )
    if current_user == None:
        flash( "This email doesn't exists in our DB.", "error_login_email" )
        return redirect( "/" )
    if User.validate_password( request.form["password"], current_user.password ) == False:
        return redirect( "/" )
    session["user_id"] = current_user.id
    session["full_name"] = current_user.first_name + " " + current_user.last_name
    session["team_id"] = current_user.team_id
    return redirect( "/welcome" ) 

@app.route( "/account/<int:id>" )
def proccess_update(id):
    if "user_id" not in session:
        return redirect( "/")
    data = {
        "users_id": id
    }
    current_user = User.get_one_user(data)
    return render_template("account.html", current_user=current_user)

@app.route( "/user/account/<int:id>", methods=['POST'] )
def update_user( id ):
    if User.validate_user_again( request.form ) == False:
        return redirect( f"/account/{id}" )
    update_user = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "team_id" : request.form["team_id"],
        "email" : request.form["email"],
        "users_id" : id
    }
    User.update_one( update_user )
    return redirect( "/" )

@app.route( "/logout", methods=["POST"] )
def process_logout():
    session.clear()
    return redirect( "/" )