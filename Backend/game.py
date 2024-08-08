import os
import google.generativeai as genai
import random

# Configure the generative AI
genai.configure(api_key=os.environ["API_KEY"])

model = genai.GenerativeModel('gemini-1.5-pro')

# Define Genres, Roles, and Situations
genres = ["Pirate", "Medieval", "Sci-Fi", "Fantasy"]
roles = {
    "Pirate": ["Captain", "Navigator", "Cannoneer", "Swordman"],
    "Medieval": ["Knight", "Archer", "Mage", "Healer"],
    "Sci-Fi": ["Commander", "Pilot", "Engineer", "Soldier"],
    "Fantasy": ["Warrior", "Ranger", "Sorcerer", "Bard"]
}

situations = {
    "Pirate": ["Kraken attack", "Enemy ship attack", "Storm", "Treasure hunt"],
    "Medieval": ["Dragon attack", "Castle siege", "Bandit ambush", "Quest for a relic"],
    "Sci-Fi": ["Alien invasion", "Spaceship malfunction", "Asteroid collision", "Search for a new planet"],
    "Fantasy": ["Orc raid", "Dark forest adventure", "Cursed artifact", "Rescue mission"]
}

# Generate a random scenario
def generate_scenario(genre, num_players):
    situation = random.choice(situations[genre])
    player_roles = random.sample(roles[genre], num_players)
    return situation, player_roles

# Generate the background story with player responsibilities and user perspective
def generate_background_story(genre, situation, player_roles, player_names):
    prompt = (
        f"Dungeon Master: The {genre.lower()} setting is fraught with danger as {situation} unfolds. "
        f"Your party must quickly react to the situation at hand.\n\n"
    )

    for i, (role, name) in enumerate(zip(player_roles, player_names)):
        prompt += (
            f"**{name} ({role}):** You have specific responsibilities in this dire situation.\n\n"
            f"* **Responsibility 1:** Describe an action that fits your role in the context of the {situation}.\n"
            f"* **Responsibility 2:** Consider the well-being of the group while carrying out your tasks.\n"
            f"* **Responsibility 3:** Evaluate any risks and potential rewards in your actions.\n\n"
        )

    prompt += (
        "The situation intensifies, and every decision could mean the difference between survival and doom. "
        "What will you do?"
    )
    
    response = model.generate_content(prompt)
    return response.text

# Generate the final story and song based on player actions
def generate_final_story_and_song(genre, situation, player_roles, player_names, player_actions):
    prompt = f"In a {genre} adventure, your group of friends faced a {situation}. "
    for name, role, action in zip(player_names, player_roles, player_actions):
        prompt += f"{name} ({role}) decided to {action}. "
    prompt += (
        "Write an engaging story about their adventure, including outcomes such as who survived, who got injured, and if they gained anything. "
        "Additionally, create a song inspired by the story in an appropriate style. Respond in JSON format with fields 'story', 'song', and 'song_style'."
    )
    
    response = model.generate_content(prompt)
    return response.text

# Example Usage
genre = "Pirate"
num_players = 4
player_names = ["Alice", "Bob", "Charlie", "Diana"]
situation, player_roles = generate_scenario(genre, num_players)
background_story = generate_background_story(genre, situation, player_roles, player_names)

print("Dungeon Master:", background_story)

# Collect player actions
player_actions = []
for name, role in zip(player_names, player_roles):
    action = input(f"{name} ({role}), what will you do? ")
    player_actions.append(action)

print("Player Actions:", player_actions)

# Generate final output
final_output = generate_final_story_and_song(genre, situation, player_roles, player_names, player_actions)
print("Final Output:", final_output)
