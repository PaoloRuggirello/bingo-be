from bingo.Utils import db


def save(bingo_paper):
    db.session.add(bingo_paper)
    db.session.commit()