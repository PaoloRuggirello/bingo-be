from bingo.Utils import app, db, socketio
from bingo.User import User
from dto.BingoPaperDTO import BingoPaperDTO
from bingo.BingoPaper import BingoPaper
from controller.RoomController import room_controller
from controller.UserController import user_controller
from flask_socketio import join_room, emit, rooms, send
from flask import request


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
    number = 52
    socketio.send({"messsage":"This is my message"}, json=True, room="Myroom")
    print("Message sent")
    return "First room added"


@socketio.on("message")
def extract_number(data):
    print("Received message: " + data)
    #socketio.emit("IOresponse", "This is the reposnse")

@socketio.on("join_room")
def join(data):
    room_code = data["room_code"]
    user_nickname = data["user_nickname"]
    join_room(room_code, sid=request.sid)
    send(f"{user_nickname} joined the room, sid: {request.sid}", room=room_code)


def register_blueprints():
    app.register_blueprint(room_controller, url_prefix='/room')
    app.register_blueprint(user_controller, url_prefix='/user')


if __name__ == '__main__':
    db.create_all()
    register_blueprints()
    socketio.run(app)