from flask import Blueprint, request
from dto.BingoPaperDTO import BingoPaperDTO
import helper.RoomHelper as rh
import repository.RoomRepository as rr

paper_controller = Blueprint('paper_controller', __name__)

"""
This Controller contains endpoints useful for obtain information or perform operation on bingo-papers
"""


@paper_controller.route('/next/<room_code>', methods=['POST'])
def next_paper_excluding(room_code):
    exclude_ids = request.json['exclude'] if request.json is not None else []
    room = rr.find_by_code(room_code)
    if room is not None:
        bingo_paper = rh.get_first_available_paper_in_room(room, exclude_ids)
        return BingoPaperDTO(bingo_paper).toJSON()
    else:
        return 'Room not found', 404
