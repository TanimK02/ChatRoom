from sqlalchemy.exc import SQLAlchemyError
from models import RoomModel, ChannelModel, user_rooms
from flask_login import login_required
from socket_handler import socketio
from schemas import CreateChannelSchema, EditChannelSchema, DeleteChannelSchema
from db import db
from flask import session
from flask_smorest import Blueprint, abort
from flask import flash

channel_blp = Blueprint("Channels", "channels", description="Operations on channels")

@channel_blp.route("/create_channel", methods=["POST"])
@login_required
@channel_blp.arguments(CreateChannelSchema)
def create_channel(data):
    room = db.session.execute(db.select(RoomModel).where(RoomModel.id==data["room"])).scalar_one_or_none()
    user = session.get('_user_id')
    if room:
        roles = room.roles 
    if room and (user in roles["Owner"] or user in roles["Admins"]):
        
        channel = ChannelModel(name=data["name"], room_id=room.id)
        room.channels.append(channel)
        try:
            db.session.add(room)
            db.session.commit()
            socketio.emit("channels_update", CreateChannelSchema(many=True).dump(room.channels.all()), to=room.id)
            return {"message": "creation successful"}, 200 
        except SQLAlchemyError:
            abort(400, message="Something went wrong creating the channel.")
    else:
        abort(400, message="Room does not exist or you don't have the necessary role.")

@channel_blp.route("/delete_channel/" , methods=["DELETE"])
@login_required
@channel_blp.arguments(DeleteChannelSchema)
def delete_channel(data):
    room = db.session.execute(db.select(RoomModel).where(RoomModel.id==data["room"])).scalar_one_or_none()
    user = session.get('_user_id')
    roles = room.roles
    if room and (user in roles["Owner"] or user in roles["Admins"]):
        if len(room.channels.all()) == 1:
            abort(400, message="Can't delete last channel")
        channel = db.session.execute(db.select(ChannelModel).where(ChannelModel.id==data["channel_id"]).where(ChannelModel.room_id==room.id)).scalar_one_or_none()
        if channel:
            try:
                db.session.delete(channel)
                db.session.commit()
                socketio.close_room(channel.id)
                socketio.emit("channels_update", CreateChannelSchema(many=True).dump(room.channels.all()), to=room.id)
                return {"message": "delete successful"}, 200
            except SQLAlchemyError:
                abort(400, message="Something went wrong deleting the channel.")
        else:
            abort(400, message="Channel doesn't exist.")
    else:
        abort(400, message="Room does not exist or you don't have the necessary role.")


@channel_blp.route("/edit_channel", methods=["PUT"])
@login_required
@channel_blp.arguments(EditChannelSchema)
def edit_channel(data):
    room = db.session.execute(db.select(RoomModel).where(RoomModel.id==data["room"])).scalar_one_or_none()
    user = session.get('_user_id')
    roles = room.roles
    if room and (user in roles["Owner"] or user in roles["Admins"]):
        channel = db.session.execute(db.select(ChannelModel).where(ChannelModel.id==data["channel_id"]).where(ChannelModel.room_id==room.id)).scalar_one_or_none()
        if channel:
            channel.name = data["new_name"]
            try:
                db.session.add(channel)
                db.session.commit()
                socketio.emit("channels_update", CreateChannelSchema(many=True).dump(room.channels.all()), to=room.id)
                return {"message": "edit successful"}, 200 
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
    room = db.session.execute(db.select(RoomModel).where(RoomModel.id==id)).scalar()
    if db.session.execute(db.select(user_rooms).where(user_rooms.c.user==user).where(user_rooms.c.room==id)).scalar_one_or_none() or not room.password:
        return room.channels.all()