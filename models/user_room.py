from db import db

user_rooms = db.Table('user_rooms',
    db.Column('user', db.String, db.ForeignKey('users.id'), primary_key=True),
    db.Column('room', db.String, db.ForeignKey('rooms.id'), primary_key=True)
)

