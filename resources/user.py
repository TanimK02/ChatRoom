from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from models import UserModel
from schemas import UserForm

from db import db
from flask import request, current_app, render_template
from flask_smorest import Blueprint, abort
import re
import bcrypt

user_blp = Blueprint("Users", "users", description="operations on users")

@user_blp.route("/")
@user_blp.route("/login")
class HomeOrLogin(MethodView):
    def get(self):
        return render_template("index.html")
    

@user_blp.route("/sign_up")
class SignUp(MethodView):
    def get(self):
        form = UserForm()
        return render_template("sign-up.html", form=form)
    
    
    def post(self):
        form = UserForm(request.form)
        print(form.errors)
        if form.validate_on_submit():
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
            return render_template("index.html", success="Account Made Sucessfully!")
        else:
            return render_template("sign-up.html", form=form)