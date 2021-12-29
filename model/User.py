from bingo.Utils import db
from sqlalchemy.orm import relationship


class User(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    nickname = db.Column('nickname', db.String(20))
    room_id = db.Column('room_id', db.ForeignKey('room.id'))
    cards = relationship("Card")

    def __init__(self, nickname, room_id):
        self.nickname = nickname
        self.room_id = room_id

