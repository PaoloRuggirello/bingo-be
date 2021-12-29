from bingo.Utils import db
from sqlalchemy.orm import relationship


class User(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    nick_name = db.Column('nick_name', db.String(20))
    cards = relationship("Card")

    def __init__(self, nick_name):
        self.nick_name = nick_name

