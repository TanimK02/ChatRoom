from flask import Flask, request, redirect, url_for
from flask_cors import CORS
from flask_login import LoginManager
from flask_smorest import Api, abort
from flask_migrate import Migrate
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import UserModel
from socket_handler import socketio
from resources.user import user_blp
from resources.rooms import room_blp
from resources.channel import channel_blp
import logging
import sys
import os

def create_app():
    app = Flask(__name__)
    logging.basicConfig(level=logging.DEBUG)
    app.config["API_TITLE"] = "Blog REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.1.0"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config['WTF_CSRF_ENABLED'] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///../example.db'
    app.config['SECRET_KEY'] = "12dsfaa"
    CORS(app)
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        try:
            return db.session.execute(db.select(UserModel).where(UserModel.id == id)).scalar_one()
        except SQLAlchemyError:
            return None
        
    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect(url_for('Users.HomeOrLogin'))


    socketio.init_app(app, cors_allowed_origins="*")

    db.init_app(app)
    with app.app_context():
        db.create_all()
    api = Api(app)
    api.register_blueprint(user_blp)
    api.register_blueprint(room_blp)
    api.register_blueprint(channel_blp)
    # logger = logging.getLogger('sqlalchemy')
    # logger.setLevel(logging.DEBUG)
    # console_handler = logging.StreamHandler(sys.stdout)
    # console_handler.setLevel(logging.DEBUG)
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # console_handler.setFormatter(formatter)
    # logger.addHandler(console_handler)
    return app

app = create_app()

if __name__ == "__main__":
    socketio.run(app, debug=True)
