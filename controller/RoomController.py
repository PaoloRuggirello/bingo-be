from flask import Blueprint
from model.Room import Room
import repository.RoomRepository as rp
room_controller = Blueprint('room_controller', __name__)


@room_controller.route("/room/new/<room_name>", methods=['POST'])
def create_room(room_name):
    room = Room(room_name)
    rp.save(room)
    return room.code

