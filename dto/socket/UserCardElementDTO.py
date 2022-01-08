class UserCardElementDTO:

    def __init__(self, user_nickname, card_id):
        self.user_nickname = user_nickname
        self.card_id = card_id

    def __iter__(self):
        yield 'user_nickname', self.user_nickname
        yield 'card_id', self.card_id
