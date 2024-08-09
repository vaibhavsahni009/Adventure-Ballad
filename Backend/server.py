from flask import Flask, request, session, jsonify
from flask_socketio import join_room, leave_room, send, SocketIO
from flask_cors import CORS
import random
from string import ascii_uppercase
import threading
import time
from src.game import Game_Model
from src.suno import suno

app = Flask(__name__)
app.config["SECRET_KEY"] = "hjhjsdahhds"
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

rooms = {}
MIN_USERS = 2
# Assume Game_model is defined elsewhere and imported


def generate_unique_code(length):
    """Generate a unique room code."""
    while True:
        code = "".join(random.choices(ascii_uppercase, k=length))
        if code not in rooms:
            return code


def validate_session():
    """Validate the user's session."""
    room = session.get("room")
    name = session.get("name")
    if not room or not name or room not in rooms or name not in rooms[room]["members"]:
        return None, None, "Invalid session."
    return room, name, None


def send_server_message(room, message):
    """Send a message from the server to the specified room."""
    if room in rooms:
        content = {"name": "Server", "message": message}
        send(content, to=room)
        rooms[room]["messages"].append(content)
        print(f"Server sent to room {room}: {message}")


@app.route("/", methods=["POST"])
def home():
    """Handle user creation and joining rooms."""
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

    if create:
        room = generate_unique_code(4)
        rooms[room] = {
            "members": {},
            "messages": [],
            "admin": name,
            "started": False,
            "game_model": Game_Model(),
        }
    else:
        room = code
        if room not in rooms:
            return jsonify({"error": "Room does not exist."}), 400

    session.update({"room": room, "name": name})
    rooms[room]["members"][name] = time.time()
    return jsonify({"room": room})


@socketio.on("start_game")
def start_game(data):
    """Start the game if conditions are met."""
    room, name, error = validate_session()
    if error:
        send({"name": "Server", "message": error}, room=request.sid)
        return

    if rooms[room]["admin"] != name:
        send(
            {"name": "Server", "message": "Only the admin can start the game."},
            room=request.sid,
        )
        return

    if len(rooms[room]["members"]) < MIN_USERS:
        send(
            {
                "name": "Server",
                "message": f"At least {MIN_USERS} users are required to start the game.",
            },
            room=request.sid,
        )
        return

    start_message = data.get("message", "The game has started!")
    genre = data.get("genre", "default")
    rooms[room]["started"] = True
    send_server_message(room, start_message)
    print(f"Admin {name} started the game with message: {start_message}")

    game_model = rooms[room]["game_model"]
    num_players = len(rooms[room]["members"])
    situation, player_roles = game_model.generate_scenario(genre, num_players)
    player_names = list(rooms[room]["members"].keys())
    background_stories = game_model.generate_background_story(
        genre, situation, player_roles, player_names
    )

    # Store game data in the room
    rooms[room].update(
        {
            "situation": situation,
            "player_roles": player_roles,
            "background_stories": background_stories,
            "num_players": num_players,
            "player_names": player_names,
        }
    )

    for user in player_names:
        user_story = background_stories[user]
        send({"name": "Server", "scenario": user_story}, to=user)


@socketio.on("submit_action")
def submit_action(data):
    """Handle user actions and generate final story if all actions are submitted."""
    room, name, error = validate_session()
    if error:
        send({"name": "Server", "message": error}, room=request.sid)
        return

    action = data.get("action", "No action")
    rooms[room].setdefault("player_actions", {})[name] = action
    print(f"{name} submitted action: {action}")

    if len(rooms[room]["player_actions"]) == rooms[room]["num_players"]:
        # Generate the final story and song
        game_model = rooms[room]["game_model"]
        genre = data.get("genre", "default")
        prefix, suffix = game_model.get_suffix_prefix(rooms[room]["background_stories"])
        final_story, song = game_model.generate_final_story_and_song(
            genre,
            rooms[room]["situation"],
            rooms[room]["player_roles"],
            rooms[room]["player_names"],
            rooms[room]["player_actions"],
            prefix,
            suffix,
        )
        # Todo add sun code here
        suno(song)
        send_server_message(room, final_story)
        # Optionally send the song to the players or handle it as needed


@socketio.on("connect")
def connect():
    """Handle a new user connection."""
    room, name, error = validate_session()
    if error:
        return

    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"][name] = time.time()
    print(f"{name} joined room {room}")


@socketio.on("disconnect")
def disconnect():
    """Handle user disconnection."""
    room = session.get("room")
    name = session.get("name")
    if not room:
        return

    leave_room(room)

    if room in rooms:
        if name in rooms[room]["members"]:
            del rooms[room]["members"][name]
            message = f"{name} has left the room"
            if name == rooms[room]["admin"]:
                message += " (admin)"
            send({"name": "System", "message": message}, to=room)
        if not rooms[room]["members"]:
            del rooms[room]

    print(f"{name} disconnected from room {room}")


def check_user_activity():
    """Check for inactive users and disconnect them."""
    while True:
        current_time = time.time()
        for room, data in list(rooms.items()):
            inactive_members = [
                member
                for member, join_time in data["members"].items()
                if current_time - join_time > 5
            ]
            for member in inactive_members:
                send(
                    {
                        "name": "Server",
                        "message": f"{member} has been disconnected due to inactivity.",
                    },
                    room=room,
                )
                leave_room(room)
                del data["members"][member]
        time.sleep(5)


if __name__ == "__main__":
    thread = threading.Thread(target=check_user_activity)
    thread.daemon = True
    thread.start()
    socketio.run(app, debug=True)
