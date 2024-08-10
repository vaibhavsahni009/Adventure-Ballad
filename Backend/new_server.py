from flask import Flask, request, session, jsonify
from flask_socketio import join_room, leave_room, send, SocketIO
from flask_cors import CORS
import random
from string import ascii_uppercase
import threading
import time
from src.game import Game_Model
from src.suno import suno
import logging
import copy

app = Flask(__name__)
app.config["SECRET_KEY"] = "hjhjsdahhds"
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")


rooms = {}
MIN_USERS = 2


def generate_unique_code(length):
    """Generate a unique room code."""
    while True:
        code = "".join(random.choices(ascii_uppercase, k=length))
        if code not in rooms:
            return code


def validate_session(room):
    if room in rooms:
        return rooms[room], None
    else:
        return None, "Invalid session"


@app.route("/", methods=["POST"])
def home():
    """Handle user creation and joining rooms."""
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
            "members": {
                name: {
                    "joined_at": time.time(),
                    "last_active": time.time(),
                    "role": None,
                    "response": None,
                    "action_prompts": None,
                },
            },
            "messages": [],
            "admin": name,
            "started": False,
            "game_model": Game_Model(),
        }
    else:
        room = code
        if room not in rooms:
            return jsonify({"error": "Room does not exist."}), 400
        rooms[room]["members"][name] = {
            "joined_at": time.time(),
            "last_active": time.time(),
            "role": None,
            "response": None,
        }
    # rooms[room]["members"][name] = time.time()
    return jsonify({"room": room, "user_name": name})


@app.route("/start_game", methods=["POST"])
def start_game():
    """Start the game if conditions are met."""
    # room, name, error = validate_session()
    data = request.json
    room = data.get("code")
    name = data.get("name")
    # if error:
    #     return jsonify({"name": "Server", "type": "error", "message": error}), 400

    if rooms[room]["admin"] != name:
        return (
            jsonify(
                {
                    "name": "Server",
                    "type": "error",
                    "message": "Only the admin can start the game.",
                }
            ),
            403,
        )

    if len(rooms[room]["members"]) < MIN_USERS:
        return (
            jsonify(
                {
                    "name": "Server",
                    "type": "error",
                    "message": f"At least {MIN_USERS} users are required to start the game.",
                }
            ),
            400,
        )

    genre = data.get("genre", "random")
    rooms[room]["started"] = True
    game_model = rooms[room]["game_model"]
    num_players = len(rooms[room]["members"])

    situation, player_roles = game_model.generate_scenario(genre, num_players)
    player_names = list(rooms[room]["members"].keys())

    background_stories = game_model.generate_background_story(
        genre, situation, player_roles, player_names
    )
    background_stories_json = game_model.get_json_from_text(background_stories)
    # for i in range(0,len(player_roles)):
    for i, player in enumerate(list(rooms[room]["members"].values())):
        player["role"] = player_roles[i]
        player["action_prompts"] = background_stories_json.get(player["role"])
    rooms[room]["background_story_raw"] = background_stories
    rooms[room]["situation"] = situation
    rooms[room]["prefix"], rooms[room]["suffix"] = game_model.get_suffix_prefix(
        background_stories
    )
    rooms[room]["num_players"] = num_players

    print(player_roles)
    print(background_stories)
    print(situation)
    # Todo get roles and situations in right format

    # Store game data in the room
    # rooms[room].update(
    #     {
    #         "situation": situation,
    #         "player_roles": player_roles,
    #         "background_stories": background_stories,
    #         "num_players": num_players,
    #         "player_names": player_names,
    #     }
    # )

    # Create a response dictionary for each user
    response_data = {}
    # for user in player_names:
    #     user_story = background_stories[user]
    #     # Send the scenario to the user via WebSocket or add it to the response
    #     # send({"name": "Server", "scenario": user_story}, to=user)
    #     response_data[user] = {"scenario": user_story}

    return jsonify(response_data), 200


@app.route("/fetch_scenario", methods=["GET"])
def fetch_scenario():
    data = request.json
    room = data.get("code")
    name = data.get("name")
    response = {
        "room": room,
        "user_name": name,
        "data": rooms[room]["members"].get(name),
    }
    print("jhgdasjfgjhgasdjgj")
    print(rooms)
    print(response)
    return jsonify(response), 200


@app.route("/fetch_room_details", methods=["GET"])
def fetch_room_details():
    data = request.json
    room = data.get("code")
    new_dict = {}
    for key, value in rooms[room].items():
        if key != "game_model":
            new_dict[key] = value

    return jsonify({"room": new_dict}), 200


@app.route("/submit_action", methods=["POST"])
def submit_action():
    """Handle user actions and generate final story if all actions are submitted."""
    data = request.json
    room = data.get("code")
    name = data.get("name")
    action = data.get("action", "No action")

    rooms[room].setdefault("player_actions", {})[name] = action

    print(f"{name} submitted action: {action}")

    # Check if all players have submitted their actions
    if len(rooms[room]["player_actions"]) == rooms[room]["num_players"]:
        game_model = rooms[room]["game_model"]
        genre = request.json.get("genre", "default")

        # Generate the prefix and suffix for the story
        prefix, suffix = game_model.get_suffix_prefix(rooms[room]["background_stories"])

        # Generate the final story and song
        final_story, song = game_model.generate_final_story_and_song(
            genre=genre,
            situation=rooms[room]["situation"],
            player_roles=rooms[room]["player_roles"],
            player_names=rooms[room]["player_names"],
            player_actions=rooms[room]["player_actions"],
            prefix=prefix,
            suffix=suffix,
        )
        rooms[room]["story"] = final_story
        rooms[room]["song"] = song
        # Call a function to handle the song (e.g., play or save)
        suno(song)

        # Send the final story back to all users via WebSocket
        # send_server_message(room, final_story)

        return (
            jsonify({"status": "success", "final_story": final_story, "song": song}),
            200,
        )

    # If not all players have submitted their actions
    return (
        jsonify({"status": "pending", "message": f"Action from {name} recorded."}),
        200,
    )


if __name__ == "__main__":
    socketio.run(app, debug=True)
