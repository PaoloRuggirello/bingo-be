from bingo.Utils import db


def save(user):
    db.session.add(user)
    db.session.commit()