from typing import Optional, Dict
from db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

class ChannelModel(db.Model):
    __tablename__ = "channels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    rooms = relationship("RoomModel", back_populates='channels')