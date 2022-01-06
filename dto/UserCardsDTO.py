import json
from dto.CardDTO import CardDTO


class UserCardsDTO:

    def __init__(self, cards):
        self.cardDTOs = [CardDTO(card) for card in cards]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)