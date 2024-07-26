from db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
import uuid
from sqlalchemy.exc import SQLAlchemyError
from flask_login import UserMixin
import bcrypt

class UserModel(db.Model, UserMixin):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(60), nullable=False)
    pic_url: Mapped[str] = mapped_column(nullable=True)
    rooms = relationship("RoomModel", back_populates='users', secondary="user_rooms", lazy='dynamic')
    @staticmethod
    def get_user(username, password):
        try:
            user = db.session.execute(db.select(UserModel).where(UserModel.username == username)).scalar_one()
            if bcrypt.checkpw(password.encode('utf-8'), user.password):
                return user
            else:
                return None
        except SQLAlchemyError:
            return None