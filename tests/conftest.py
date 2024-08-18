import pytest
from app import create_app, db
from flask_login import FlaskLoginClient
from models import UserModel
import bcrypt


@pytest.fixture
def redis_client(request):
    import fakeredis
    redis_client = fakeredis.FakeRedis()
    return redis_client

@pytest.fixture()
def app(redis_client):
    app = create_app()
    app.config["TESTING"] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.r = redis_client
    app.test_client_class = FlaskLoginClient
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def logged_client(app):
    user = UserModel(
                username = "bazookas123",
                password = bcrypt.hashpw("bazookas12893".encode("utf-8"), bcrypt.gensalt()),
                email = "bazjkokas@gmail.com"
            )
    db.session.add(user)
    db.session.commit()
    return app.test_client(user=user)

@pytest.fixture()
def false_client(app):
    user = UserModel(
                username = "batman567",
                password = bcrypt.hashpw("bazookas12893".encode("utf-8"), bcrypt.gensalt()),
                email = "batmankas@gmail.com"
            )
    db.session.add(user)
    db.session.commit()
    return app.test_client(user=user)

@pytest.fixture(autouse=True)
def setup_database(app):
    from app import db
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()

