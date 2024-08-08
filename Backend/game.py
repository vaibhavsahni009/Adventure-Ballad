import os
import google.generativeai as genai
import random

# Configure the generative AI
genai.configure(api_key=os.environ["API_KEY"])

model = genai.GenerativeModel('gemini-1.5-pro')

# Define Genres, Roles, and Situations
genres = ["Pirate", "Medieval", "Sci-Fi", "Fantasy"]
roles = {
    "Pirate": ["Captain", "Quartermaster", "Cannoneer", "Navigator", "Cook"],
    "Medieval": ["Knight", "Archer", "Mage", "Healer"],
    "Sci-Fi": ["Commander", "Pilot", "Engineer", "Medic"],
    "Fantasy": ["Warrior", "Ranger", "Sorcerer", "Bard"]
}

situations = {
    "Pirate": [
        # "Kraken attack", 
        "Enemy ship attack"
        # , "Storm", "Treasure hunt"
        ],
    "Medieval": ["Dragon attack", "Castle siege", "Bandit ambush", "Quest for a relic"],
    "Sci-Fi": ["Alien invasion", "Spaceship malfunction", "Asteroid collision", "Search for a new planet"],
    "Fantasy": ["Orc raid", "Dark forest adventure", "Cursed artifact", "Rescue mission"]
}

def generate_scenario(genre, num_players):
    situation = random.choice(situations[genre])
    player_roles = random.sample(roles[genre], num_players)
    return situation, player_roles

def generate_background_story(genre, situation, player_roles):
    prompt = (
        f"Dungeon Master: The {genre.lower()} setting is fraught with danger as {situation} unfolds. "
        f"Your party must quickly react to the situation at hand.\n\n"
    )

    for i, role in enumerate(player_roles):
        prompt += (
            f"**Player {i+1} ({role}):** You have specific responsibilities in this dire situation.\n\n"
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

def generate_final_story_and_song(genre, situation, player_roles, player_actions):
    prompt = (
        f"In this {genre} adventure, a group of players faces the challenge of a {situation}. "
        f"Each player took their own unique approach:\n\n"
    )

    for role, action in zip(player_roles, player_actions):
        prompt += f"* **{role}:** {action}\n"

    prompt += (
        "\nBased on these actions, create an engaging story about their journey. Include the outcomes for each character, "
        "such as who survived, who was injured, and whether they succeeded in their goals. Additionally, generate a song "
        "inspired by the story, in an appropriate style. Please respond in JSON format with fields 'story', 'song', and 'song_style'."
    )
    
    response = model.generate_content(prompt)
    return response.text

# Example Usage
genre = "Pirate"
num_players = 4
situation, player_roles = generate_scenario(genre, num_players)
background_story = generate_background_story(genre, situation, player_roles)

print("Dungeon Master:", background_story)

# Collect player actions
player_actions = []
for role in player_roles:
    action = input(f"What will the {role} do? ")
    player_actions.append(action)

print("Player Actions:", player_actions)

# Generate final output
final_output = generate_final_story_and_song(genre, situation, player_roles, player_actions)
print("Final Output:", final_output)
