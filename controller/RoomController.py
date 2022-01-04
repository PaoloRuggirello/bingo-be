from flask import Blueprint
from bingo.Room import Room
from bingo.User import User
from dto.BingoPaperDTO import BingoPaperDTO
from dto.CreatedRoomDTO import CreatedRoomDTO
import repository.RoomRepository as rr
import repository.UserRepository as ur
from helper.RoomHelper import *

room_controller = Blueprint('room_controller', __name__)


@room_controller.route("/create/<room_name>/<host_nickname>", methods=['POST'])
def create_room(room_name, host_nickname):
    room = Room(room_name)
    rr.save(room)
    room_host = User(host_nickname, room.id)
    ur.save(room_host)
    bank_bingo_paper = generate_bank_bingo_paper(room.id, room_host.id)
    bpr.save(bank_bingo_paper)
    return CreatedRoomDTO(room.code, room.name, BingoPaperDTO(bank_bingo_paper).toJSON()).toJSON()


@room_controller.route("/join/<room_code>/<user_nickname>", methods=['POST'])
def join_room(room_code, user_nickname):
    room = rr.find_by_code(room_code)
    if not is_nickname_unique_in_room(room, user_nickname):
        return f"Duplicate nickname {user_nickname} in room with code {room_code}", 400  # Returns bad request
    new_user = User(user_nickname, room.id)
    ur.save(new_user)
    paper_to_return = get_first_available_paper_in_room(room)
    paper_to_return = remove_assigned_cards_from_paper(paper_to_return)
    return BingoPaperDTO(paper_to_return).toJSON()