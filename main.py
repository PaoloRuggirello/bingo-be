from bingo.Utils import app, db, socketio
from bingo.Room import Room
from bingo.User import User
from dto.BingoPaperDTO import BingoPaperDTO
from bingo.BingoPaper import BingoPaper
from controller.RoomController import room_controller
from controller.UserController import user_controller


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


def register_blueprints():
    app.register_blueprint(room_controller, url_prefix='/room')
    app.register_blueprint(user_controller, url_prefix='/user')


if __name__ == '__main__':
    db.create_all()
    register_blueprints()
    socketio.run(app)
