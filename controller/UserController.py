from flask import Blueprint, request
from repository import RoomRepository as rr
from repository import CardRepository as cr
from helper import RoomHelper as room_helper
from helper import UserHelper as user_helper
from dto.UserCardsDTO import UserCardsDTO

user_controller = Blueprint('user_controller', __name__)

"""
This Controller contains endpoints useful for obtain information or perform operation on users
"""


@user_controller.route("/card/assign/<room_code>/<user_nickname>", methods=['POST'])
def assign_cards(room_code, user_nickname):
    """
    This service is used to assign a list of cards to the specified user
    @param room_code: the code of the room
    @param user_nickname: the nickname of the involved user
    """
    room = rr.find_by_code(room_code)
    if room is not None:
        user = room_helper.get_user_from_room(room, user_nickname)
        if user is None:
            return "Forbidden! Given user doesn't exists in room!", 403
        card_ids_to_assign = request.json['cards']
        cards = cr.find_by_card_id_in(card_ids_to_assign)
        already_assigned_cards = user_helper.assign_cards_to_user(user, cards)
        return (already_assigned_cards.dumps(), 400) if len(already_assigned_cards) > 0 else ('Success', 200)
    else:
        return "Room not found", 404


@user_controller.route("/<room_code>/<user_nickname>/cards", methods=['GET'])
def get_user_cards(room_code, user_nickname):
    """
    This service is used to obtain the list of cards assigned to a specified user
    @param room_code: the code of the room
    @param user_nickname: the nickname of the involved user
    @return: the list of cards assigned to the specified user
    """
    room = rr.find_by_code(room_code)
    if room is not None:
        user_in_room = list(filter(lambda user: user.nickname == user_nickname, room.users))
        if len(user_in_room) == 1:
            return UserCardsDTO(user_in_room[0].cards).toJSON()
        else:
            return "User not found", 404
    else:
        return "Room not found", 404



