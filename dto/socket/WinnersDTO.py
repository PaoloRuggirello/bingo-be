class WinnersDTO:
    def __init__(self, winners, win_type):
        self.winners = winners
        self.win_type = win_type

    def __iter__(self):
        yield 'winners', [dict(winner) for winner in self.winners]
        yield 'win_type', self.win_type
