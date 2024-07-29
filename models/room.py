
from db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, JSON, Integer
import uuid

class RoomModel(db.Model):
    __tablename__ = "rooms"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(20), nullable=True)
    roles = mapped_column(JSON, nullable=False)
    people: Mapped[int] = mapped_column(Integer(), nullable=False)
    users = relationship("UserModel", back_populates='rooms', secondary="user_rooms", lazy='dynamic')
    channels = relationship("ChannelModel", back_populates='rooms', lazy='dynamic', cascade='all, delete')
