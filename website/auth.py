from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/sign-in",methods = ["GET", "POST"])
def sign_in():
    if current_user.is_authenticated:
        flash("You are already signed in", category="error")
        return redirect(url_for("views.home"))

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        correct = True 
        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Signed in successfully", category="success")
                login_user(user, remember= True)
                return redirect(url_for("views.home"))
            else:
                correct = False
        else:
            correct = False

        if not correct:
            flash("Email or password is wrong, try again!", category="error")
        
    return render_template("sign-in.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.sign_in"))


@auth.route("/sign-up", methods = ["GET", "POST"])
def sign_up():
    if current_user.is_authenticated:
        flash("You are already signed in", category="error")
        return redirect(url_for("views.home"))
    if request.method == "POST":
        
        data = request.form
        fullname = data["fullname"]
        email = data["email"]
        password1 = data["password1"]
        password2 = data["password2"]

        success = True
        user = User.query.filter_by(email = email).first()
        if user:
            success = False
            flash("Email already exists", category="error")
        if len(fullname) < 5:
            success = False
            flash("Full name must be longer than 5 characters", category="error")
        if len(fullname) > 100:
            success = False
            flash("Full name mustn't longer than 100 characters", category="error")    
        if "@" not in email:
            success = False
            flash("Email must contain \"@\"", category="error")
        if len(email) >= 150:
            success = False
            flash("Email mustn't longer than 150 characters", category="error")
        if not 8 <= len(password1) <=30:
            flash("Password must length between 8 and 30 characters", category="error")
        if password1 != password2:
            success = False
            flash("Confirm password does not match", category="error")
        if success:
            flash("Account created", category="success")
            new_user = User(email = email, fullname = fullname, password = generate_password_hash(password1) )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("auth.sign_in"))
        
    
    return render_template("sign-up.html")