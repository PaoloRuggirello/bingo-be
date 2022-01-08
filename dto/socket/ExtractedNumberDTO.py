class ExtractedNumberDTO:
    def __init__(self, number):
        self.number = number

    def __iter__(self):
        yield 'number', str(self.number)
