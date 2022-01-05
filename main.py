from bingo.Utils import app, db, socketio
from controller.RoomController import room_controller
from controller.UserController import user_controller
from controller.BingoPaperController import paper_controller
from flask_socketio import join_room, emit, leave_room
from flask import request

users_subscriptions = {}


@socketio.on("join_room")
def join(data):
    global users_subscriptions
    room_code = data["room_code"]
    user_nickname = data["user_nickname"]
    user_sid = request.sid
    if user_sid in users_subscriptions:
        if room_code == users_subscriptions[user_sid][1]:
            emit("ErrorMessage", {"msg": f"{user_nickname} already in room: {users_subscriptions[user_sid][1]}."})
        else:
            emit("ErrorMessage", {"msg":f"{user_nickname} is already parts of room with code: {users_subscriptions[user_sid][1]}... You need to leave your current room to join another on"})
    else:
        join_room(room_code, sid=request.sid)
        users_subscriptions[user_sid] = [user_nickname, room_code]
        emit("RoomServiceMessages", {'msg': user_nickname + ' joined.'}, room=room_code)


@socketio.on("leave_room")
def leave(data):
    global users_subscriptions
    user_subscription = users_subscriptions[request.sid]
    user_nickname = user_subscription[0]
    room_code = user_subscription[1]
    emit("RoomServiceMessages", {"msg":f"{user_nickname} left the room"}, room=room_code)
    leave_room(room_code, request.sid)
    del users_subscriptions[request.sid]


def register_blueprints():
    app.register_blueprint(room_controller, url_prefix='/room')
    app.register_blueprint(user_controller, url_prefix='/user')
    app.register_blueprint(paper_controller, url_prefix='/paper')


if __name__ == '__main__':
    db.create_all()
    register_blueprints()
    print("Bingo online")
    socketio.run(app)
