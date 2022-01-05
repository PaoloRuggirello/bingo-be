from bingo.Utils import db
from bingo.Card import Card


def find_by_card_id_in(card_ids):
    return db.session.query(Card).filter(Card.id.in_(card_ids)).all()


def find_by_card_id(card_id):
    return Card.query.filter_by(id=card_id).first()


def save_all(cards):
    map(lambda card: db.session.add(card), cards)
    db.session.commit()


def delete_cards_by_id_in(card_ids):
    db.session.query(Card).filter(Card.id.in_(card_ids)).delete()
    db.session.commit()
