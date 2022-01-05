from flask import Blueprint
from bingo.Room import Room
from bingo.User import User
from dto.BingoPaperDTO import BingoPaperDTO
from dto.CreatedRoomDTO import CreatedRoomDTO
from dto.JoinedRoomDTO import JoinedRoomDTO
import repository.RoomRepository as rr
import repository.UserRepository as ur
from helper.RoomHelper import *
from bingo.Utils import get_random_room_code, socketio, PAPER_NUMBERS, db
import numpy as np
from random import choice

room_controller = Blueprint('room_controller', __name__)


@room_controller.route("/create/<room_name>/<host_nickname>", methods=['POST'])
def create_room(room_name, host_nickname):
    room_unique_code = get_random_room_code(6)
    room = Room(room_name, room_unique_code)
    rr.save(room)
    room_host = User(host_nickname, room.id)
    ur.save(room_host)
    bank_bingo_paper = generate_bank_bingo_paper(room.id, room_host.id)
    bpr.save(bank_bingo_paper)
    return CreatedRoomDTO(room_unique_code, room.code, room.name, BingoPaperDTO(bank_bingo_paper)).toJSON()


@room_controller.route("/join/<room_code>/<user_nickname>", methods=['POST'])
def join_room(room_code, user_nickname):
    room = rr.find_by_code(room_code)
    if room is None:
        return 'Invalid room code. Room not found!', 404
    elif not game_already_started(room):
        if not is_nickname_unique_in_room(room, user_nickname):
            return f"Duplicate nickname {user_nickname} in room with code {room_code}", 400  # Returns bad request
        new_user = User(user_nickname, room.id)
        ur.save(new_user)
        paper_to_return = get_first_available_paper_in_room(room)
        paper_to_return = remove_assigned_cards_from_paper(paper_to_return)
        return JoinedRoomDTO(room.name, BingoPaperDTO(paper_to_return)).toJSON()
    else:
        return 'Cannot join. Game already started', 403


@room_controller.route("/extract/<room_code>/<unique_code>", methods=['POST'])
def extract_number(room_code, unique_code):
    room = rr.find_by_code(room_code)
    if room is not None:
        if room.unique_code != unique_code:
            return "Wrong unique code!", 403
        is_first_extraction = not game_already_started(room)
        if is_first_extraction:
            remove_unused_cards(room)
        extract_numbers_indexes = room.extracted_numbers - 1 if not is_first_extraction else []
        remaining_numbers = np.delete(PAPER_NUMBERS, extract_numbers_indexes)
        extracted_number = choice(remaining_numbers)
        room.extracted_numbers = np.append(room.extracted_numbers, extracted_number) if not is_first_extraction else np.array([extracted_number], dtype=np.int8)
        rr.commit()
        socketio.emit("ExtractedNumber", {"number": str(extracted_number)}, room=room_code)
        return str(extracted_number)
    else:
        return "Room not found", 400
