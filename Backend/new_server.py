from flask import Flask, request, session, jsonify
from flask_socketio import join_room, leave_room, send, SocketIO
from flask_cors import CORS
import random
from string import ascii_uppercase

# import threading
import time
from src.game import Game_Model
from src.suno import suno

# import logging
import json

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
    adventure_type = data.get("adventure_type", False)
    if join:
        print("Join")

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
                    "player_action": None,
                    "action_prompts": None,
                },
            },
            "game_started": False,
            "admin": name,
            "started": False,
            "game_model": Game_Model(),
            "player_reponses": 0,
            "adventure_type": adventure_type,
        }
    else:
        room = code
        if room not in rooms:
            print("room unavailable")
            return jsonify({"error": "Room does not exist."}), 400
        rooms[room]["members"][name] = {
            "joined_at": time.time(),
            "last_active": time.time(),
            "role": None,
            "response": None,
        }
    # rooms[room]["members"][name] = time.time()
    players = list(rooms[room]["members"].keys())
    return jsonify({"roomCode": room, "user_name": name, "players": players})


@app.route("/start_game", methods=["POST"])
def start_game():
    """Start the game if conditions are met."""
    data = request.json
    room = data.get("code")
    name = data.get("name")

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
    rooms[room]["game_started"] = True
    genre = rooms[room].get("adventure_type")
    print(f"Genre {genre}")
    rooms[room]["started"] = True
    game_model = rooms[room]["game_model"]
    num_players = len(rooms[room]["members"])

    situation, player_roles = game_model.generate_scenario(genre, num_players)
    player_names = list(rooms[room]["members"].keys())

    background_stories = game_model.generate_background_story(
        genre, situation, player_roles, player_names
    )
    background_stories_json = game_model.get_json_from_text(background_stories)
    keys = list(background_stories_json.keys())
    new_dict = {}
    for key in keys:
        new_key = key.split(" ")[0].split("_")[0]
        print(new_key)
        new_dict[new_key] = background_stories_json[key]
    for i, player in enumerate(list(rooms[room]["members"].values())):
        player["role"] = player_roles[i]
        player["action_prompts"] = new_dict.get(player["role"])

    rooms[room]["background_story_raw"] = background_stories
    rooms[room]["background_story"] = new_dict
    rooms[room]["situation"] = situation
    rooms[room]["prefix"], rooms[room]["suffix"] = game_model.get_prefix_suffix(
        background_stories
    )
    rooms[room]["num_players"] = num_players
    response_data = {}
    return jsonify(response_data), 200


@app.route("/fetch_player_data", methods=["POST"])
def fetch_player_data():
    data = request.json
    room = data.get("code")
    name = data.get("name")
    response = {
        "room": room,
        "user_name": name,
        "data": rooms[room]["members"].get(name),
    }
    return jsonify(response), 200


@app.route("/api/rooms/<room_code>", methods=["GET"])
def get_room(room_code):
    # Retrieve room data from the dictionary based on room_code
    room = rooms.get(room_code)

    if room is None:
        # Return a 404 error if the room_code is not found
        return jsonify(404, description="Room not found")
    players = list(room["members"].keys())
    return (
        jsonify(
            {
                "players": players,
                "admin": room["admin"],
                "game_started": room["game_started"],
            }
        ),
        200,
    )


@app.route("/fetch_scenario/<room>/<name>", methods=["GET"])
def fetch_scenario(room, name):
    if rooms[room].get("prefix"):
        try:
        
            item = rooms[room]["members"].get(name).get("action_prompts").values()
            user_responsibility = ""
            for I in item:
                user_responsibility = f"{user_responsibility} \n {I}"
        except:
            user_responsibility = rooms[room]["members"].get(name).get("action_prompts")
        user_responsibility = f"{rooms[room]['prefix']} \n {user_responsibility} \n {rooms[room]['suffix']}"
        response = {
            "room": room,
            "user_name": name,
            # "data": rooms[room]["members"].get(name),
            "scenario_published": True,
            "role": rooms[room]["members"].get(name).get("role"),
            "text": f"{user_responsibility} ",
        }
        return jsonify(response), 200
    else:
        response = {
            "room": room,
            "user_name": name,
            "scenario_published": False,
            "text": "Please wait Scenario is being genrated",
        }
    return jsonify(response), 200

@app.route("/fetch_room_details/<room>", methods=["GET"])
def fetch_room_details(room):
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
    rooms[room]["player_reponses"] += 1
    rooms[room]["members"][name]["player_action"] = action
    print(f"{name} submitted action: {action}")

    # Check if all players have submitted their actions
    if rooms[room]["player_reponses"] == rooms[room]["num_players"]:
        print("now")
        game_model = rooms[room]["game_model"]
        genre = request.json.get("genre", "default")

        player_names = list(rooms[room]["members"].keys())
        player_roles = []
        player_actions = []

        for player in player_names:
            player_roles.append(rooms[room]["members"][player].get("role"))
            player_actions.append(rooms[room]["members"][player].get("player_action"))

        response = game_model.generate_final_story_and_song(
            genre=genre,
            situation=rooms[room]["situation"],
            player_roles=player_roles,
            player_names=player_names,
            player_actions=player_actions,
            prefix=rooms[room]["prefix"],
            suffix=rooms[room]["suffix"],
        )
        response_dict = game_model.get_json_from_text(response)
        final_story = response_dict.get("story")
        song = response_dict.get("song")
        rooms[room]["story"] = final_story
        rooms[room]["song"] = song
        try:
            rooms[room]["song_suno"] = suno(response_dict)
            print("song", rooms[room]["song_suno"])
        except:
            pass
        return (
            jsonify({"status": "success", "final_story": final_story, "song": song}),
            200,
        )

    else:
        print("Not yet")
    # If not all players have submitted their actions
    return (
        jsonify({"status": "pending", "message": f"Action from {name} recorded."}),
        200,
    )


@app.route("/fetch_final_story/<room>", methods=["GET"])
def fetch_final_story(room):
    return jsonify({"final_story": rooms[room].get("story")}), 200


@app.route("/fetch_final_song/<room>", methods=["GET"])
def fetch_final_song(room):
    return jsonify({"song": rooms[room].get("song_suno")}), 200


if __name__ == "__main__":
    socketio.run(app, debug=True)
