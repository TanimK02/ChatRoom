from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from models import UserModel
from schemas import UserSchema
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