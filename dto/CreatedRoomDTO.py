import json


class CreatedRoomDTO:

    def __init__(self, room_code, bingo_paper_dto):
        self.room_code = room_code
        self.bingo_paper_dto = bingo_paper_dto

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)