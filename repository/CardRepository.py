from bingo.Utils import db
from bingo.Card import Card


def find_by_card_id_in(card_ids):
    return db.session.query(Card).filter(Card.id.in_(card_ids)).all()


def save_all(cards):
    map(lambda card: db.session.add(card), cards)
    db.session.commit()