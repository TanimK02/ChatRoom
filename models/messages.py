
from db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


class MessageModel(db.Model):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(nullable=False)
    channel_id: Mapped[str] = mapped_column(ForeignKey("channels.id"))
    username: Mapped[str] = mapped_column(nullable=False)
    channel = relationship("ChannelModel", back_populates='messages')