from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from models import RoomModel, ChannelModel
from flask_login import login_required, current_user
from socket_handler import socketio
from schemas import RoomForm, RoomsReturnSchema
from db import db
from flask import request, current_app, render_template, url_for, redirect, session
from flask_smorest import Blueprint, abort
from flask import flash

room_blp = Blueprint("Rooms", "rooms", description = "Operations on rooms")


@room_blp.route("/room/create")
class RoomOps(MethodView):

    @login_required
    def post(self):
        form = RoomForm(request.form)
        if form.validate_on_submit():
            if len(current_user.rooms.all()) >= 10:
                return {"error": "Can't make any more rooms"}, 400
            check = db.session.execute(db.select(RoomModel.name).where(RoomModel.name==form.name.data)).scalar_one_or_none()
            if check:
                return {"error": "room name taken"}
            room = RoomModel(
                name = form.name.data,
                roles = {"Owner": f"{current_user.id}",
                         "Admins": []},
                people = 0
            )
            room.users.append(current_user)
            
            if hasattr(form, "password"):
                room.password = form.password.data
            try:
                db.session.add(room)
                db.session.commit()
            except SQLAlchemyError:
                return {"error": "something went wrong while creating room"}, 400
            general = ChannelModel(name = "general", room_id = room.id)
            try:
                db.session.add(general)
                db.session.commit()
                return {"room" : form.name.data}
            except SQLAlchemyError:
                db.session.delete(room)
                db.session.commit()
                return {"error": "something went wrong while creating room"}, 400
        else:
            return {"error": "Form not filled correctly"}, 400


@room_blp.route("/rooms/", defaults={'page': 1})
@room_blp.route("/rooms/<int:page>")
@login_required
@room_blp.response(200, RoomsReturnSchema(many=True))
def loadRooms(page):
    page -= 1
    if page < 0:
        page = 0
    try:
        page *= 10
        return db.session.execute(db.select(RoomModel).limit(10).offset(page).order_by(RoomModel.people.desc())).scalars()
    except SQLAlchemyError:
        abort(400, message="Something went wrong looking for rooms.")


@room_blp.route("/my_rooms")
@login_required
@room_blp.response(200, RoomsReturnSchema(many=True))
def myRooms():
    try:
        return current_user.rooms.all()
    except SQLAlchemyError:
        abort(400, message="Something went wrong getting your rooms.")


@room_blp.route("/delete_room/<int:id>")
@login_required
def deleteRoom(id):
    if not isinstance(id, int):
        abort(400, message="needs to be int.")
    room = db.session.get(RoomModel, id)
    if not room:
        abort(400, message="Room doesn't exist.")
    if room.roles["Owner"] == session.get('_user_id'):
        try:
            socketio.close_room(room.name)
            db.session.delete(room)
            db.session.commit()
            return {"Status": "Success"}, 200
        except SQLAlchemyError:
            abort(400, message="Something went wrong while deleting the room.")