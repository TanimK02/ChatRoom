
from db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
import uuid

class ChannelModel(db.Model):
    __tablename__ = "channels"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    room_id: Mapped[str] = mapped_column(ForeignKey("rooms.id"))
    rooms = relationship("RoomModel", back_populates='channels')
    messages = relationship("MessageModel", back_populates='channel', lazy='dynamic', cascade='all, delete')
