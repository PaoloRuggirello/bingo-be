import json
import numpy as np
from dto.CardDTO import CardDTO


class BingoPaperDTO:

    def __init__(self, bingo_paper):
        self.bingo_paper_id = str(bingo_paper.id)
        self.cardDTOs = np.empty(shape=(0))
        self.color = bingo_paper.color
        for card in bingo_paper.cards:
            self.cardDTOs = np.append(self.cardDTOs, CardDTO(card))
        self.number_of_cards = len(self.cardDTOs)
        self.cardDTOs = self.cardDTOs.tolist()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)