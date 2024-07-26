from sqlalchemy.exc import SQLAlchemyError
from models import RoomModel, ChannelModel, user_rooms
from flask_login import login_required
from socket_handler import socketio
from schemas import CreateChannelSchema, EditChannelSchema
from db import db
from flask import session
from flask_smorest import Blueprint, abort
from flask import flash

channel_blp = Blueprint("Channels", "channels", descriptions="Operations on channels")

@channel_blp.route("/create_channel")
@login_required
@channel_blp.arguments(CreateChannelSchema)
def create_channel(data):
    room = db.session.execute(db.select(RoomModel).where(RoomModel.id==data["room"])).scalar_one_or_none
    user = session.get('_user_id')
    roles = room.roles

    if room and (user in roles["Owner"] or user in roles["Admin"]):
        channel = ChannelModel(name=data["name"], room_id=room.id)
        room.channels.append(channel)
        try:
            db.session.add(room)
            db.session.commit()
        except SQLAlchemyError:
            abort(400, message="Something went wrong creating the channel.")
    else:
        abort(400, message="Room does not exist or you don't have the necessary role.")

@channel_blp.route("/delete_channel/")
@login_required
@channel_blp.arguments(CreateChannelSchema)
def delete_channel(data):
    room = db.session.execute(db.select(RoomModel).where(RoomModel.id==data["room"])).scalar_one_or_none
    user = session.get('_user_id')
    roles = room.roles
    if room and (user in roles["Owner"] or user in roles["Admin"]):
        channel = db.session.execute(db.select(ChannelModel).where(ChannelModel.name==data["name"]).where(ChannelModel.room_id==room.id)).scalar_one_or_none
        if channel:
            try:
                db.session.delete(channel)
                db.session.commit()
                socketio.close_room(channel.id)
            except SQLAlchemyError:
                abort(400, message="Something went wrong deleting the channel.")
        else:
            abort(400, message="Channel doesn't exist.")
    else:
        abort(400, message="Room does not exist or you don't have the necessary role.")


@channel_blp.route("/edit_channel")
@login_required
@channel_blp.arguments(EditChannelSchema)
def delete_channel(data):
    room = db.session.execute(db.select(RoomModel).where(RoomModel.id==data["room"])).scalar_one_or_none
    user = session.get('_user_id')
    roles = room.roles
    if room and (user in roles["Owner"] or user in roles["Admin"]):
        channel = db.session.execute(db.select(ChannelModel).where(ChannelModel.name==data["name"]).where(ChannelModel.room_id==room.id)).scalar_one_or_none
        if channel:
            channel.name = data["new_name"]
            try:
                db.session.add(channel)
                db.session.commit()
            except SQLAlchemyError:
                abort(400, message="Something went wrong editing the channel.")
        else:
            abort(400, message="Channel doesn't exist.")
    else:
        abort(400, message="Room does not exist or you don't have the necessary role.")


@channel_blp.route("/load_channels/<string:id>")
@login_required
@channel_blp.response(200, CreateChannelSchema(many=True))
def load_channels(id):
    user = session.get('_user_id')
    if db.session.execute(db.select(user_rooms).where(user_rooms.c.user==user).where(user_rooms.c.room==id)).scalar_one_or_none():
        return db.session.execute(db.select(RoomModel).where(RoomModel.id==id)).scalar().channels.all()