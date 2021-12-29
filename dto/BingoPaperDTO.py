import json
import numpy as np
from dto.CardDTO import CardDTO


class BingoPaperDTO:

    def __init__(self, bingo_paper):
        self.cardDTOs = np.empty(shape=(0))
        for card in bingo_paper.cards:
            self.cardDTOs = np.append(self.cardDTOs, CardDTO(card))
        self.cardDTOs = self.cardDTOs.tolist()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)