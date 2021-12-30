import numpy as np

from repository import CardRepository as cr


def assign_cards_to_user(user, cards):
    already_assigned = np.empty(shape=0)
    assigned_to_user = np.empty(shape=0)
    for card in cards:
        if card.user_id is None:
            card.user_id = user.id
            assigned_to_user = np.append(assigned_to_user, card)
        else:
            already_assigned = np.append(already_assigned, int(card.id))
    cr.save_all(assigned_to_user)
    return already_assigned