from bingo.Utils import socketio
from flask_socketio import join_room, send, emit
from flask import request


# @socketio.on("join_room")
# def join(data):
#     room_code = data["room_code"]
#     user_nickname = data["user_nickname"]
#     join_room(room_code, sid=request.sid)
#     send(f"{user_nickname} joined the room, sid: {request.sid}", room=room_code)



