from flask import Blueprint
from model.Room import Room
from model.User import User
from bingo.BingoPaper import BingoPaper
from dto.BingoPaperDTO import BingoPaperDTO
from dto.CardDTO import CardDTO
import repository.RoomRepository as rp
import repository.UserRepository as ur

room_controller = Blueprint('room_controller', __name__)


@room_controller.route("/new/<room_name>", methods=['POST'])
def create_room(room_name):
    room = Room(room_name)
    rp.save(room)
    return room.code


@room_controller.route("/join/<room_code>/<user_nickname>", methods=['POST'])
def join_room(room_code, user_nickname):
    room = rp.find_by_code(room_code)
    new_user = User(user_nickname, room.id)
    ur.save(new_user)
    return BingoPaperDTO(BingoPaper()).toJSON()