from bingo.Utils import db
from bingo.Room import Room


def save(room):
    db.session.add(room)
    db.session.commit()


def find_by_code(room_code):
    return Room.query.filter_by(code=room_code).first()