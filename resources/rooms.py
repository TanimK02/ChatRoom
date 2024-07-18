from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from models import RoomModel
from flask_login import login_required, current_user
from flask_socketio import disconnect
from schemas import RoomForm, RoomsReturnSchema
from db import db
from flask import request, current_app, render_template, url_for, redirect
from flask_smorest import Blueprint, abort
from flask import flash

room_blp = Blueprint("Rooms", "rooms", description = "Operations on rooms")


@room_blp.route("/room/create")
class RoomOps(MethodView):

    @login_required
    def post(self):
        form = RoomForm(request.form)
        if form.validate_on_submit():
            check = db.session.execute(db.select(RoomModel.name).where(RoomModel.name==form.name.data)).scalar_one_or_none()
            if check:
                return {"error": "room name taken"}
            room = RoomModel(
                name = form.name.data,
                roles = {"Owner": f"{current_user.id}",
                         "Admins": []},
                people = 1
            )
            if hasattr(form, "password"):
                room.password = form.password.data
            try:
                db.session.add(room)
                db.session.commit()
                return {"room" : form.name.data}
            except SQLAlchemyError:
                return {"error": "something went wrong while creating room"}
        else:
            return {"status": "Form not filled correctly"}, 400


@room_blp.route("/rooms/<int:page>", defaults={"page": 1})
@login_required
@room_blp.response(200, RoomsReturnSchema(many=True))
def rooms(page):
    page = -1
    if page < 0:
        page = 0
    try:
        page *= 10
        return db.session.execute(db.select(RoomModel).limit(10).offset(page).order_by(RoomModel.people.desc())).scalars()
    except SQLAlchemyError:
        abort(400, message="Something went wrong looking for rooms.")