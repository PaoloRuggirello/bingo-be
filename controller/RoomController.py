from flask import Blueprint
from bingo.Room import Room
from bingo.User import User
from dto.BingoPaperDTO import BingoPaperDTO
from dto.CreatedRoomDTO import CreatedRoomDTO
from dto.JoinedRoomDTO import JoinedRoomDTO
from helper import CardHelper as ch
import repository.UserRepository as ur
from helper.RoomHelper import *
from bingo.Utils import get_random_room_code, socketio, db, PRIZE_LIST, users_subscriptions
from random import choice
from bingo.Prize import Prize
from dto.socket.UpdatedCardsDTO import UpdatedCardsDTO
from dto.socket.WinnersDTO import WinnersDTO
from dto.socket.ExtractedNumberDTO import ExtractedNumberDTO
from helper.SocketTypeEnum import SocketTypeEnum

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
    room = rr.find_by_code(room_code.upper())
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
        if room.current_prize_index < 5:
            if len(remaining_numbers) > 0:
                extracted_number = choice(remaining_numbers)
                room.last_extracted_number = extracted_number
                print(dict(ExtractedNumberDTO(extracted_number)))
                socketio.emit(SocketTypeEnum.ExtractedNumber.value, dict(ExtractedNumberDTO(extracted_number)), room=room_code)
                add_extracted_number_to_room(room, is_first_extraction, extracted_number)
                updated_cards_list = []
                winners_list = []
                for paper in room.papers:
                    current_card_and_winner = \
                        paper.get_cards_with_number_and_winner(extracted_number, PRIZE_LIST[room.current_prize_index])
                    up_cards_list, w_list = \
                        ch.set_number_as_extracted_in_card(current_card_and_winner, paper.cards, room)
                    updated_cards_list.extend(up_cards_list)
                    winners_list.extend(w_list)

                if len(updated_cards_list) > 0:
                    print(f"UpdatedCards: {dict(UpdatedCardsDTO(updated_cards_list))}")
                    socketio.emit(SocketTypeEnum.UpdatedCard.value, dict(UpdatedCardsDTO(updated_cards_list)),
                                  room=room.code)
                if len(winners_list) > 0:
                    prize_name = Prize(PRIZE_LIST[room.current_prize_index]).name
                    print(f"Winners: {dict(WinnersDTO(winners_list, prize_name))}")
                    socketio.emit(SocketTypeEnum.WinnerEvent.value, dict(WinnersDTO(winners_list, prize_name)), room=room.code)
                    room.current_prize_index += 1

                db.session.commit()
                return str(extracted_number)
            else:
                return "All numbers already extracted", 200
        else:
            return "Game ended, all prizes assigned", 200
    else:
        return "Room not found", 400


@room_controller.route("/last_extracted_number/<room_code>", methods=['GET'])
def last_extracted_number(room_code):
    room = rr.find_by_code(room_code)
    if room is not None:
        if room.last_extracted_number is not None:
            print(f"Request last extracted number, {room.last_extracted_number}")
            return str(room.last_extracted_number)
        else:
            return "No numbers already extracted"
    else:
        return "Room not found", 400


@room_controller.route("/online_players/<room_code>", methods=['GET'])
def online_players(room_code):
    online_players_number = 0
    online_players_nicknames = []
    for user_sid in users_subscriptions:
        if users_subscriptions[user_sid][1] == room_code:
            online_players_number += 1
            online_players_nicknames.append(users_subscriptions[user_sid][0])
    return {'online_players_number':str(online_players_number), 'online_players_nicknames':online_players_nicknames}


@room_controller.route("/winners/<room_code>", methods=['GET'])
def get_room_winners(room_code):
    room = rr.find_by_code(room_code)
    if room is not None:
        return room.winners
    else:
        return "Room not found", 400


