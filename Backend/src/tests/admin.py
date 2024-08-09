import socketio
import requests
import json
import asyncio

# Constants
SERVER_URL = "http://localhost:5000"


# Helper functions
def create_room(name):
    response = requests.post(SERVER_URL, json={"name": name, "create": True})
    if response.status_code == 200:
        data = response.json()
        return data["room"]
    else:
        print(f"Error creating room: {response.json()}")
        return None


def join_room(name, room_code):
    response = requests.post(
        SERVER_URL, json={"name": name, "join": True, "code": room_code}
    )
    if response.status_code == 200:
        data = response.json()
        return data["room"]
    else:
        print(f"Error joining room: {response.json()}")
        return None


def get_room_info():
    response = requests.get(f"{SERVER_URL}/room")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error getting room info: {response.json()}")
        return None


# Initialize Socket.IO client
sio = socketio.Client()


@sio.event
def connect():
    print("Connected to server")


@sio.event
def connect_error(data):
    print(f"Connection failed: {data}")


@sio.event
def disconnect():
    print("Disconnected from server")


@sio.event
def server_message(data):
    print(f"Received message from server: {data}")


@sio.event
def error_message(data):
    """Handle error messages from the server."""
    if data.get("type") == "error":
        print(f"Error from server: {data['message']}")


async def main():
    # Connect to the server
    sio.connect("http://localhost:5000")

    # Create a room
    name = "User1"
    room_code = create_room(name)
    if room_code is None:
        return

    print(f"Room created with code: {room_code}")

    # Optionally, join the room with another user
    # room_code = join_room("User2", room_code)
    # if room_code is None:
    #     return
    # print(f"Joined room with code: {room_code}")

    # Start the game
    start_game_message = {"message": "Starting the game!", "genre": "adventure"}
    sio.emit("start_game", start_game_message)

    # Submit an action
    submit_action_message = {"action": "Exploring the cave", "genre": "adventure"}
    sio.emit("submit_action", submit_action_message)

    # Give time for the server to respond
    await asyncio.sleep(5)

    # Disconnect from the server
    sio.disconnect()


# Run the script
if __name__ == "__main__":
    asyncio.run(main())
