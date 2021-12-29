from bingo.Utils import db
from sqlalchemy.orm import relationship


class User(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    nick_name = db.Column('nick_name', db.String(20))
    room_id = db.Column('room_id', db.ForeignKey('room.id'))
    cards = relationship("Card")

    def __init__(self, nick_name, room_id):
        self.nick_name = nick_name
        self.room_id = room_id

