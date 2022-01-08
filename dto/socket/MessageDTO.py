class MessageDTO:
    def __init__(self, msg):
        self.msg = msg

    def __iter__(self):
        yield 'msg', self.msg
