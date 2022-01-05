from flask import Blueprint
from bingo.Room import Room
from bingo.User import User
from dto.BingoPaperDTO import BingoPaperDTO
from dto.CreatedRoomDTO import CreatedRoomDTO
from dto.JoinedRoomDTO import JoinedRoomDTO
import repository.RoomRepository as rr
import repository.UserRepository as ur
from helper.RoomHelper import *
from bingo.Utils import get_random_room_code, socketio, PAPER_NUMBERS, db, PRIZE_LIST
import numpy as np
from random import choice
import repository.CardRepository as cr
from sqlalchemy.orm.attributes import flag_modified
from bingo.Prize import Prize
from flask_socketio import emit

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
        remove_useless_cards_if_needed(room, is_first_extraction)
        remaining_numbers = get_remaining_numbers(room, is_first_extraction)
        if len(remaining_numbers) > 0:
            extracted_number = choice(remaining_numbers)
            add_extracted_number_to_room(room, is_first_extraction, extracted_number)
            for paper in room.papers:
                current_card_and_winner = paper.get_cards_with_number_and_winner(extracted_number, PRIZE_LIST[room.current_prize_index])
                for card_id in current_card_and_winner:
                    card_updated = list(filter(lambda card: card.id == card_id, paper.cards))[0]
                    flag_modified(card_updated, 'extracted_by_row')
                    flag_modified(card_updated, 'card_numbers')
                    involved_user = list(filter(lambda user: user.id == card_updated.user_id, room.users))[0]
                    socketio.emit("UpdatedCard", {"user_nickname": f"{involved_user.nickname}", "card_id": f"{card_updated.id}"}, room=room_code)
                    if current_card_and_winner[card_id]:
                        socketio.emit("WinnerEvent", {"user_nickname":f"{involved_user.nickname}", "win_type": f"{Prize(PRIZE_LIST[room.current_prize_index]).name}", "card_id": f"{card_updated.id}"}, room=room_code)
                        room.current_prize_index += 1
            db.session.commit()
            socketio.emit("ExtractedNumber", {"number": str(extracted_number)}, room=room_code)
            return str(extracted_number)
        else:
            return "All numbers already extracted", 200
    else:
        return "Room not found", 400
