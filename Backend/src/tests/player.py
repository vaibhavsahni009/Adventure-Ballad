import asyncio
import websockets
import requests
import json

# Constants
SERVER_URL = "http://localhost:5000"
WEB_SOCKET_URL = "ws://localhost:5000/socket.io/?EIO=4&transport=websocket"


# Helper functions
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


async def send_websocket_message(message):
    async with websockets.connect(WEB_SOCKET_URL) as websocket:
        await websocket.send(message)
        response = await websocket.recv()
        print(f"Received: {response}")


async def main():
    # Join the room
    name = "Player1"
    room_code = "ROOM_CODE"  # Replace with the actual room code
    joined_room_code = join_room(name, room_code)
    if joined_room_code is None:
        return

    print(f"Joined room with code: {joined_room_code}")

    # Start the game (assuming the game is started by the admin and this is to simulate the player side)
    start_game_message = json.dumps(
        {"type": "start_game", "message": "Starting the game!", "genre": "adventure"}
    )
    await send_websocket_message(start_game_message)

    # Submit an action
    submit_action_message = json.dumps(
        {"type": "submit_action", "action": "Exploring the cave", "genre": "adventure"}
    )
    await send_websocket_message(submit_action_message)


# Run the script
if __name__ == "__main__":
    asyncio.run(main())
