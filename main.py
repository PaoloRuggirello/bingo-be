from bingo.Utils import app, db, socketio
from bingo.User import User
from dto.BingoPaperDTO import BingoPaperDTO
from bingo.BingoPaper import BingoPaper
from controller.RoomController import room_controller
from controller.UserController import user_controller
from flask_socketio import join_room, emit, leave_room
from flask import request

users_subscriptions = {}


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


@socketio.on("join_room")
def join(data):
    global users_subscriptions
    room_code = data["room_code"]
    user_nickname = data["user_nickname"]
    user_sid = request.sid
    if user_sid in users_subscriptions:
        emit("ErrorMessage", {"msg":f"{user_nickname} is already parts of room with code: {users_subscriptions[user_sid][1]}... You need to leave your current room to join another on"})
    else:
        join_room(room_code, sid=request.sid)
        users_subscriptions[user_sid] = [user_nickname, room_code]
        emit("RoomMessages", {'msg': user_nickname + ' has entered the room.'}, room=room_code)


@socketio.on("leave_room")
def leave(data):
    global users_subscriptions
    user_subscription = users_subscriptions[request.sid]
    user_nickname = user_subscription[0]
    room_code = user_subscription[1]
    emit("RoomMessages", {"msg":f"{user_nickname} left the room"}, room=room_code)
    leave_room(room_code, request.sid)
    del users_subscriptions[request.sid]


def register_blueprints():
    app.register_blueprint(room_controller, url_prefix='/room')
    app.register_blueprint(user_controller, url_prefix='/user')


if __name__ == '__main__':
    db.create_all()
    register_blueprints()
    socketio.run(app)