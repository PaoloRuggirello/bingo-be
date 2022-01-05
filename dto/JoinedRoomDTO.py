import json


class JoinedRoomDTO:

    def __init__(self, room_name, bingo_paper_dto):
        self.room_name = room_name
        self.bingo_paper_dto = bingo_paper_dto

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)