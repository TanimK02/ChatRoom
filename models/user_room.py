from db import db

user_rooms = db.Table('user_rooms',
    db.Column('user', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('room', db.Integer, db.ForeignKey('rooms.id'), primary_key=True)
)

