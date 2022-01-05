from bingo.BingoPaper import BingoPaper
import repository.BingoPaperRepository as bpr
import repository.CardRepository as cr


def is_nickname_unique_in_room(room, nickname):
    nicknames_in_room = [user.nickname for user in room.users]
    return not nickname in nicknames_in_room


def get_first_available_paper_in_room(room, exclude_ids=None):
    if len(room.papers) > 0:
        for paper in room.papers:
            if exclude_ids is None or paper.id not in exclude_ids:
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
    bank_bingo_paper = BingoPaper(room_id, True)
    for card in bank_bingo_paper.cards:
        card.user_id = host_id
    return bank_bingo_paper


def game_already_started(room):
    return room.extracted_numbers is not None and len(room.extracted_numbers) > 0


def remove_unused_cards(room):
    cards_to_delete = []
    for paper in room.papers:
        if not paper.is_host:
            for card in paper.cards:
                if card.user_id is None:
                    cards_to_delete.append(card.id)
    cr.delete_cards_by_id_in(cards_to_delete)
