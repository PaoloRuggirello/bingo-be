from bingo.Utils import db
from model.Room import Room


def save(room):
    db.session.add(room)
    db.session.commit()


def find_by_code(looking_room_code):
    return Room.query.filter_by(code=looking_room_code).first()