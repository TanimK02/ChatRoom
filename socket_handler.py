from flask_socketio import SocketIO, join_room, leave_room, emit, rooms
from flask import request, session, current_app
from flask_login import current_user
from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import RoomModel, user_rooms, ChannelModel, MessageModel
socketio = SocketIO()

@socketio.on('message_json')
def handle_message(data):
    if not isinstance(data, dict):
        return False
    if data["channel"] in rooms(request.sid):
        if data["message"] == "":
            return
        channel = data['channel']
        message = data['message']
        if data.get("img", None):
            img = data['img']
        else:
            img = None
        emit('message_json', {"message" : current_user.username + ": " + message,
                            "img": img}, to=channel)
        
        messageStore = MessageModel(text=message, channel_id=channel)
        channelStore = db.session.get(ChannelModel, channel)
        if channelStore:
            try:
                channelStore.messages.append(messageStore)
                db.session.add(channelStore)
                db.session.commit()
            except SQLAlchemyError:
                current_app.logger.info("didn't store message")
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
        room = db.session.execute(db.select(RoomModel).where(RoomModel.id==data.get("room"))).scalar_one_or_none()   
        if room:
            channel = ""
            if not data.get("channel_id", None):
                channel = db.session.execute(db.select(ChannelModel).where(ChannelModel.room_id==room.id).where(ChannelModel.name=="general")).scalar_one_or_none()
                if channel:
                    channel = channel.id
                else:
                    channel = db.session.execute(db.select(ChannelModel).where(ChannelModel.room_id==room.id)).first()[0].id
            else:
                channel = db.session.execute(db.select(ChannelModel.id).where(ChannelModel.id==data["channel_id"]).where(ChannelModel.room_id==room.id)).scalar_one_or_none()
                if not channel:
                    return
            username = current_user.username
            admin = False
            user_id = session.get('_user_id')
            roles = room.roles
            if user_id in roles["Owner"] or user_id in roles["Admins"]:
                admin = True
            if room.password:
                    check = db.session.execute(db.select(user_rooms).where(user_rooms.c.user==session.get('_user_id')).where(user_rooms.c.room==room.id)).scalar_one_or_none()
                    if not check:
                        if room.password == data.get("password", None):
                            room.people += 1
                            try:
                                room.users.append(current_user)
                                db.session.add(room)
                                db.session.commit()
                            except SQLAlchemyError:
                                return False
                        else:
                            return emit('join', False, to=request.sid)
                    join_room(channel)
                    join_room(room.id)
                    emit('join', {"room": room.name, "channel_id": channel, "room_id": room.id, "admin": admin}, to=request.sid)
                    emit('message_json', {"message" : username + " joined the channel"}, to=channel)
                    return
            join_room(channel)
            join_room(room.id)
            room.people += 1
            try:
                db.session.add(room)
                db.session.commit()
            except SQLAlchemyError:
                return emit('join', False, to=request.sid)
            emit('join', {"room": room.name, "channel_id": channel, "room_id": room.id, "admin": admin}, to=request.sid)
            emit('message_json', {"message" : username + " joined the channel"}, to=channel)
        else:
            return emit('join', False, to=request.sid)
    else:
        return emit('join', False, to=request.sid)

@socketio.on('leave')
def on_leave(data):
    room = data['room']
    if room in rooms(request.sid):
        leave_room(room)
        emit('message_json', {"message" : current_user.username + " left the channel"}, to=room)


@socketio.on('connect')
def connect():
    if not current_user.is_authenticated:
        return False
    