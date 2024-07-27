from flask_socketio import SocketIO, join_room, leave_room, emit, rooms
from flask import request
from flask_login import current_user
from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import RoomModel, user_rooms, ChannelModel
socketio = SocketIO()

@socketio.on('message_json')
def handle_message(data):
    if not isinstance(data, dict):
        return False
    if data["room"] in rooms(request.sid):
        if data["message"] == "":
            return
        room = data['room']
        message = data['message']
        if data.get("img", None):
            img = data['img']
        else:
            img = None
        emit('message_json', {"message" : current_user.username + ": " + message,
                            "img": img}, to=room)
    else:
        emit('message_json', {"message" : "not in room"}, to=request.sid)
 

@socketio.on("channels_update")
def update_channels(data):
    if not isinstance(data, dict):
        return False
    if data.get("room", None):
        if data.get("user", None):
            room = db.session.execute(db.select(RoomModel).where(RoomModel.id==data.get("room"))).scalar_one_or_none()
            if room:
                if data["user"] in room.roles["Owner"] or data["user"] in room.roles["Admin"]:
                    emit("channels_update", data["channels"], to=data["room"])


@socketio.on('join')
def on_join(data):
    if not isinstance(data, dict):
        return False
    if data.get("room", None):
        room = db.session.execute(db.select(RoomModel).where(RoomModel.name==data.get("room"))).scalar_one_or_none()
        if room:
            if not hasattr(data, "channel"):
                channel = db.session.execute(db.select(ChannelModel).where(ChannelModel.room_id==room.id).where(ChannelModel.name=="general")).scalar_one_or_none()
            else:
                channel = data["channel"]
            room_to_join = channel.id
            username = current_user.username
            if room.password:
                    check = db.session.execute(db.select(user_rooms).where(user_rooms.c.user==current_user.id).where(user_rooms.c.room==room.id)).scalar()
                    if check:
                        join_room(room_to_join)
                        join_room(room.id)
                        emit('join', {"room": data["room"], "channel_id": room_to_join, "room_id": room.id}, to=request.sid)
                        emit('message_json', {"message" : username + " joined the room"}, to=room_to_join)
                        return 
                    elif room.password == data.get("password", None):
                        room.people += 1
                        try:
                            room.users.append(current_user)
                            db.session.add(room)
                            db.session.commit()
                        except SQLAlchemyError:
                            return False
                    else:
                        return emit('join', False, to=request.sid)
                    join_room(room_to_join)
                    join_room(room.id)
                    emit('join', {"room": data["room"], "channel_id": room_to_join, "room_id": room.id}, to=request.sid)
                    emit('message_json', {"message" : username + " joined the room"}, to=room_to_join)
                    return
            join_room(room_to_join)
            join_room(room.id)
            room.people += 1
            try:
                db.session.add(room)
                db.session.commit()
            except SQLAlchemyError:
                return emit('join', False, to=request.sid)
            emit('join', {"room": data["room"], "channel_id": room_to_join, "room_id": room.id}, to=request.sid)
            emit('message_json', {"message" : username + " joined the room"}, to=room_to_join)
        else:
            return emit('join', False, to=request.sid)
    else:
        return emit('join', False, to=request.sid)

@socketio.on('leave')
def on_leave(data):
    room = data['room']
    if room in rooms(request.sid):
        leave_room(room)
        emit('message_json', {"message" : current_user.username + " left the room"}, to=room)


@socketio.on('connect')
def connect():
    if not current_user.is_authenticated:
        return False
    