from flask import Blueprint
from model.Room import Room
from model.User import User
from bingo.BingoPaper import BingoPaper
from dto.BingoPaperDTO import BingoPaperDTO
from dto.CardDTO import CardDTO
import repository.RoomRepository as rp
import repository.UserRepository as ur
from helper.RoomHelper import *

room_controller = Blueprint('room_controller', __name__)


@room_controller.route("/new/<room_name>", methods=['POST'])
def create_room(room_name):
    room = Room(room_name)
    rp.save(room)
    return room.code


@room_controller.route("/join/<room_code>/<user_nickname>", methods=['POST'])
def join_room(room_code, user_nickname):
    room = rp.find_by_code(room_code)
    if not is_nickname_unique_in_room(room, user_nickname):
        return f"Duplicate nickname {user_nickname} in room with code {room_code}", 400  # Returns bad request
    new_user = User(user_nickname, room.id)
    ur.save(new_user)
    paper_to_return = get_first_available_paper_in_room(room)
    paper_to_return = remove_assigned_cards_from_paper(paper_to_return)
    return BingoPaperDTO(paper_to_return).toJSON()