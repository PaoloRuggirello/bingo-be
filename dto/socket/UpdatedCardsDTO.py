class UpdatedCardsDTO:
    def __init__(self, updated_cards):
        self.updated_cards = updated_cards

    def __iter__(self):
        yield 'updated_cards', [dict(card) for card in self.updated_cards]
