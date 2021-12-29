from bingo.Utils import app, db
from model.Room import Room
from model.User import User
from dto.BingoPaperDTO import BingoPaperDTO
from bingo.BingoPaper import BingoPaper


@app.route("/newBingoPaper")
def hello():
    bingo_paper = BingoPaper()
    user = User("NickName", 1)
    db.session.add(bingo_paper)
    db.session.add(user)
    db.session.commit()
    return BingoPaperDTO(bingo_paper).toJSON()


@app.route("/")
def main():
    print("DB created")
    room = Room("First room")
    db.session.add(room)
    db.session.commit()
    return "First room added"


if __name__ == '__main__':
    db.create_all()
    app.run()
