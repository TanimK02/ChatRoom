from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from models import UserModel
from schemas import UserForm, LoginForm, RoomForm
from flask_login import login_user, login_required, logout_user
from flask_socketio import disconnect
from db import db
from flask import request, current_app, render_template, url_for, redirect
from flask_smorest import Blueprint, abort
from flask import flash
import re
import bcrypt

user_blp = Blueprint("Users", "users", description="operations on users")

@user_blp.route("/")
@user_blp.route("/login")
class HomeOrLogin(MethodView):
    def get(self):
        return render_template("index.html", form = LoginForm())
    
    def post(self):
        form = LoginForm(request.form)
        if form.validate_on_submit():
            
            user = db.session.execute(db.select(UserModel).where(UserModel.username==form.username.data)).scalar_one_or_none()
            if user and bcrypt.checkpw(form.password.data.encode('utf-8'), user.password):
                login_user(user)
                return redirect(url_for("Users.home"))
            else:
                flash("Username or password is wrong/doesn't exist.")
                return render_template("index.html", form = form, success="Username or password is wrong/doesn't exist.")

@user_blp.route("/home")
@login_required
def home():
    return render_template("chatroom.html", chatName="Join A Room", form = RoomForm())

@user_blp.route("/sign_up")
class SignUp(MethodView):
    def get(self):
        form = UserForm()
        return render_template("sign-up.html", form=form)
    
    
    def post(self):
        form = UserForm(request.form)
        if form.validate_on_submit():
            if db.session.execute(db.select(UserModel).where(UserModel.username == form["username"].data)).scalar_one_or_none():
                form.username.errors.append("Username already exists")
                return render_template("sign-up.html", form=form)
            user = UserModel(
                username = str(form.username.data),
                password = bcrypt.hashpw(str(form.password.data).encode("utf-8"), bcrypt.gensalt()),
                email = str(form.email.data)
            )
            try:
                db.session.add(user)
                db.session.commit()
            except SQLAlchemyError:
                return render_template("sign-up.html", form=form)
            result = db.session.execute(db.select(UserModel).where(UserModel.username == form["username"].data)).scalar_one()
            return redirect(url_for("Users.HomeOrLogin", success="Account Made Successfully"))
        else:
            return render_template("sign-up.html", form=form)

@user_blp.route("/logout")
class LogOut(MethodView):

    @login_required
    def get(self):
        logout_user()
        disconnect()
        return redirect(url_for("Users.HomeOrLogin"))
    
