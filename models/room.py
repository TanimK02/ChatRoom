from typing import Optional, Dict
from db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, JSON, Integer

class RoomModel(db.Model):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(20), nullable=True)
    roles = mapped_column(JSON, nullable=False)
    people: Mapped[int] = mapped_column(Integer(), nullable=False)