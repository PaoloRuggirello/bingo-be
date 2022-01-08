from sqlalchemy.orm.attributes import flag_modified
from bingo.Utils import PRIZE_LIST
from bingo.Prize import Prize
from helper import UserHelper, RoomHelper
from dto.socket.UserCardElementDTO import UserCardElementDTO


def set_number_as_extracted_in_card(current_card_and_winner, paper_cards, room):
    winners_list = []
    updated_cards_list = []
    for card_id in current_card_and_winner:
        card_updated = get_card_with_id_from_paper(card_id, paper_cards)
        set_extracted_fields_as_modified(card_updated)
        involved_user = UserHelper.get_user_with_id_from_list_of_users(card_updated.user_id, room.users)
        updated_cards_list.append(UserCardElementDTO(involved_user.nickname, card_updated.id))
        if current_card_and_winner[card_id]:
            prize_name = Prize(PRIZE_LIST[room.current_prize_index]).name
            winners_list.append(UserCardElementDTO(involved_user.nickname, card_updated.id))
            RoomHelper.fill_room_winners(room, prize_name, involved_user.nickname)
            flag_modified(room, 'winners')
    return updated_cards_list, winners_list


def get_card_with_id_from_paper(card_id, paper_cards):
    possible_cards = list(filter(lambda card: card.id == card_id, paper_cards))
    if len(possible_cards) == 1:
        return possible_cards[0]
    elif len(possible_cards) > 1:
        raise ValueError(f"More than one card with id {card_id} in given paper")
    else:
        raise ValueError(f"Card with id {card_id} not present.")


def set_extracted_fields_as_modified(card):
    flag_modified(card, 'extracted_by_row')
    flag_modified(card, 'card_numbers')