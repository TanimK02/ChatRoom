from flask_socketio import SocketIO, join_room, leave_room, emit, send, rooms
from flask import request
from flask_login import current_user
from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import RoomModel, user_rooms
import sys
import logging
socketio = SocketIO()

@socketio.on('message_json')
def handle_message(data):
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
 
@socketio.on('join')
def on_join(data):
    if not isinstance(data, dict):
        return False
    if data.get("room", None):
        room = db.session.execute(db.select(RoomModel).where(RoomModel.name==data.get("room"))).scalar_one_or_none()
        room_to_join= data['room']
        if room:
            if room.password:
                    check = db.session.execute(db.select(user_rooms).where(user_rooms.c.user==current_user.id).where(user_rooms.c.room==room.id)).scalar()
                    if check:
                        join_room(room_to_join)
                        emit('join', room_to_join, to=request.sid)
                    elif room.password == data.get("password", None):
                        room.people += 1
                        try:
                            room.users.append(current_user)
                            db.session.add(room)
                            db.session.commit()
                        except SQLAlchemyError:
                            return False
                    else:
                        return False
                    join_room(room_to_join)
                    emit('join', room_to_join, to=request.sid)
                    return
            join_room(room_to_join)
            room.people += 1
            try:
                db.session.add(room)
                db.session.commit()
            except SQLAlchemyError:
                return False
            emit('join', room_to_join, to=request.sid)
    else:
        return False

@socketio.on('leave')
def on_leave(data):
    username = current_user.username
    room = data['room']
    leave_room(room)
    send(username + 'has left the room', to=room)


@socketio.on('connect')
def connect():
    if not current_user.is_authenticated:
        return False
    