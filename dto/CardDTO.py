import json


class CardDTO:

    def __init__(self, card):
        self.card_numbers = card.card_numbers.tolist()
        self.color = card.color
        self.id = card.id

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
