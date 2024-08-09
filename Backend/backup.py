from flask import Flask, request, session, jsonify
from flask_socketio import join_room, leave_room, send, SocketIO
from flask_cors import CORS
import random
from string import ascii_uppercase
import threading
import time

app = Flask(__name__)
app.config["SECRET_KEY"] = "hjhjsdahhds"
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

rooms = {}


def generate_unique_code(length):
    while True:
        code = "".join(random.choice(ascii_uppercase) for _ in range(length))
        if code not in rooms:
            break
    return code


@app.route("/", methods=["POST"])
def home():
    session.clear()
    data = request.json
    name = data.get("name")
    code = data.get("code")
    join = data.get("join", False)
    create = data.get("create", False)

    if not name:
        return jsonify({"error": "Please enter a name."}), 400

    if join and not code:
        return jsonify({"error": "Please enter a room code."}), 400

    room = code
    if create:
        room = generate_unique_code(4)
        rooms[room] = {"members": {}, "messages": [], "admin": name}
    elif code not in rooms:
        return jsonify({"error": "Room does not exist."}), 400

    session["room"] = room
    session["name"] = name
    rooms[room]["members"][name] = time.time()  # Track the join time of members
    return jsonify({"room": room})


@app.route("/room", methods=["GET"])
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return jsonify({"error": "Invalid session."}), 400

    return jsonify({"code": room, "messages": rooms[room]["messages"]})


@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return

    content = {"name": session.get("name"), "message": data["data"]}
    # send(content, to=room)
    # Todo call suno and gemini
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")

    # Todo change message room contacts


@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return

    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"][name] = time.time()  # Track the join time of members
    print(f"{name} joined room {room}")


@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        del rooms[room]["members"][name]
        message = f"{name} has left the room"
        if name == rooms[room]["admin"]:
            message += " (admin)"
        send({"name": "System", "message": message}, to=room)
        if not rooms[room]["members"]:
            del rooms[room]

    print(message)


def check_user_activity():
    while True:
        for room in list(rooms.keys()):
            for member in list(rooms[room]["members"].keys()):
                if time.time() - rooms[room]["members"][member] > 5:
                    socketio.emit("disconnect", room=room)
        time.sleep(5)


def send_server_message(room, message):
    if room in rooms:
        content = {"name": "Server", "message": message}
        send(content, to=room)
        rooms[room]["messages"].append(content)
        print(f"Server sent to room {room}: {message}")


if __name__ == "__main__":
    thread = threading.Thread(target=check_user_activity)
    thread.daemon = True
    thread.start()
    socketio.run(app, debug=True)
4
