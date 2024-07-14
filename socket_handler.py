from flask_socketio import SocketIO, join_room, leave_room, emit, send
from flask import request
from flask_login import current_user

socketio = SocketIO()

@socketio.on('json')
def handle_message(json):
    username = json['username']
    room = json['room']
    message = json['message']
    send({"username": username, "message": message}, to=room)

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(username + 'has entered the room', to=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + 'has left the room', to=room)


@socketio.on('connect')
def connect():
    if not current_user.is_authenticated:
        return False
    