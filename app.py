from flask import Flask, request
from flask_smorest import Api, abort
from flask_migrate import Migrate
from sqlalchemy.exc import SQLAlchemyError
from db import db
from resources.user import user_blp

def create_app():
    app = Flask(__name__)
    app.config["API_TITLE"] = "Blog REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.1.0"
    app.config["OPENAPI_URL_PREFIX"] = "/"

    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///example.db'
    db.init_app(app)
    with app.app_context():
        db.create_all()
    api = Api(app)
    api.register_blueprint(user_blp)
    return app