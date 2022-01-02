from bingo.Utils import db


def save(bingo_paper):
    temp = bingo_paper.cards
    db.session.add(bingo_paper)
    db.session.commit()
    bingo_paper.cards = temp