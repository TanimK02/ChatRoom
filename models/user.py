from db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from sqlalchemy.exc import SQLAlchemyError
from flask_login import UserMixin
import bcrypt

class UserModel(db.Model, UserMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(String(60), nullable=False)
    pic_url: Mapped[str] = mapped_column(nullable=True)
    
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