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

# Generate the background story with player responsibilities in JSON format


def generate_background_story(genre, situation, player_roles, player_names):
    prompt = (
        f"As the Dungeon Master in a {genre.lower()} setting, a critical situation unfolds: {situation}. "
        f"The party must act swiftly to navigate through the dangers.\n\n"
        "You will generate a JSON object with the following structure:\n\n"
        "{\n"
        "  \"prefix_of_general_narration\": \"[Introduction to the situation that all players see]\",\n"
        "  \"{Role1}\": \"[Actionable prompts, responsibilities, and challenges for Player1 in Role1]\",\n"
        "  \"{Role2}\": \"[Actionable prompts, responsibilities, and challenges for Player2 in Role2]\",\n"
        "  \"...\": \"[Additional roles as needed]\",\n"
        "  \"suffix_of_general_narration\": \"[Closing narration that all players see]\"\n"
        "}\n\n"
    )

    prompt += "Prefix of the general narration: Describe the scene, setting the tone and the urgency of the situation, which all players will see.\n\n"

    for i, (player_name, role) in enumerate(zip(player_roles, player_names)):
        prompt += (
            f"{role}: The player is {player_name}, and their role is {role}. Provide specific actionable prompts that match their responsibilities in this situation. "
            f"Include at least three responsibilities or actions they must consider:\n"
            f"* **Responsibility 1:** Describe an action that fits the role in the context of the {situation}.\n"
            f"* **Responsibility 2:** Consider the well-being of the group while carrying out their tasks.\n"
            f"* **Responsibility 3:** Evaluate any risks and potential rewards in their actions.\n\n"
        )

    prompt += "Suffix of the general narration: Conclude the setup, emphasizing the urgency and the stakes. This will also be visible to all players.\n\n"

    prompt += "Generate this structured JSON output with the narrations and roles' responsibilities filled in accordingly."

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