from bingo.Utils import db


def save(room):
    db.session.add(room)
    db.session.commit()