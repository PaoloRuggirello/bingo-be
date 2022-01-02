from bingo.BingoPaper import BingoPaper
import repository.BingoPaperRepository as bpr
import numpy as np


def is_nickname_unique_in_room(room, nickname):
    nicknames_in_room = [user.nickname for user in room.users]
    return not nickname in nicknames_in_room


def get_first_available_paper_in_room(room):
    if len(room.papers) > 0:
        for paper in room.papers:
            for card in paper.cards:
                if card.user_id is None:
                    return paper
    new_bingo_paper = BingoPaper(room.id)
    bpr.save(new_bingo_paper)
    return new_bingo_paper


def remove_assigned_cards_from_paper(bingo_paper):
    filtered_paper = []
    for card in bingo_paper.cards:
        if card.user_id is None:
            filtered_paper.append(card)
    bingo_paper.cards = filtered_paper
    return bingo_paper


def get_user_from_room(room, user_nickname):
    for user in room.users:
        if user.nickname == user_nickname:
            return user
    return None


def exists_user_in_room(room, user_nickname):
    users_nicknames = [user.nickname for user in room.users]
    return user_nickname in users_nicknames


def generate_bank_bingo_paper(room_id, host_id):
    bank_bingo_paper = BingoPaper(room_id, True, True)
    for card in bank_bingo_paper.cards:
        card.user_id = host_id
    return bank_bingo_paper

