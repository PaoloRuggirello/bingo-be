from bingo.Utils import db, get_random_room_code
from sqlalchemy.orm import relationship


class Room(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    code = db.Column('code', db.String(5), unique=True)
    name = db.Column('name', db.String(20))
    extracted_numbers = db.Column('extracted_numbers', db.String(200), nullable=True)
    papers = relationship("BingoPaper")
    users = relationship("User")

    def __init__(self, name):
        self.name = name
        self.code = get_random_room_code()

