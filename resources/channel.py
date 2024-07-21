from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from models import RoomModel, ChannelModel
from flask_login import login_required, current_user
from socket_handler import socketio
from db import db
from flask import current_app
from flask_smorest import Blueprint, abort
from flask import flash

channel_blp = Blueprint("Channels", "channels", descriptions="Operations on channels")

@channel_blp.route("/create_channel")
@login_required
@channel_blp.arguments()