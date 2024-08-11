import requests

BASE_URL = "http://localhost:5000/"


def join_room(name, code):
    url = BASE_URL
    data = {"name": name, "code": code, "join": True}
    response = requests.post(url, json=data)
    return response.json()


def create_room(name):
    url = BASE_URL
    data = {"name": name, "create": True}
    response = requests.post(url, json=data)
    return response.json()


def start_game(name, code):
    url = BASE_URL + "start_game"
    data = {"name": name, "code": code}
    response = requests.post(url, json=data)
    # return response.json()


def fetch_scenario(name, code):
    url = BASE_URL + "fetch_scenario"
    data = {"name": name, "code": code}
    response = requests.get(url, json=data)
    return response.json()


def fetch_room_details(code):
    url = BASE_URL + "fetch_room_details"
    data = {"code": code}
    response = requests.get(url, json=data)
    return response.json()


def submit_action(name, code, action):
    url = BASE_URL + "submit_action"
    data = {"name": name, "code": code, "action": action}
    response = requests.post(url, json=data)
    return response.json()


# Example usage
if __name__ == "__main__":
    # Create a room
    create_response = create_room("admin_user")
    print("Create Room Response:", create_response)

    # Join the created room
    room_code = create_response["room"]
    join_response = join_room("user1", room_code)
    print("Join Room Response:", join_response)

    # Start the game
    start_game_response = start_game("admin_user", room_code, genre="Pirate")
    print("Start Game Response:")

    # Fetch the scenario for a user
    scenario_response = fetch_scenario("user1", room_code)
    print("Fetch Scenario Response:", scenario_response)

    # Fetch the room details
    room_details_response = fetch_room_details(room_code)
    print("Fetch Room Details Response:", room_details_response)

    # Submit an action
    abc = ""
    submit_action_response = submit_action("user1", room_code, action=abc)
    print("Submit Action Response:", submit_action_response)

    submit_action_response = submit_action("admin_user", room_code, action=abc)
    print("Submit Action Response:", submit_action_response)


# Todo edit get requests
