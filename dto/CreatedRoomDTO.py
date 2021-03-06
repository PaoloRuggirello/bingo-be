import json


class CreatedRoomDTO:

    def __init__(self, host_unique_code, room_code, room_name, bingo_paper_dto):
        self.host_unique_code = host_unique_code
        self.room_code = room_code
        self.room_name = room_name
        self.bingo_paper_dto = bingo_paper_dto

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)