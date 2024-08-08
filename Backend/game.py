import os
import google.generativeai as genai

# Configure the generative AI
genai.configure(api_key=os.environ["API_KEY"])

model = genai.GenerativeModel('gemini-1.5-pro')

import random

# Define Genres and Situations
genres = ["Pirate", "Medieval", "Sci-Fi", "Fantasy"]

situations = {
    "Pirate": [
        # "Kraken attack", 
               "Enemy ship attack"
            #    , "Storm", "Treasure hunt", "Mutiny", "Deserted island"
               ],
    "Medieval": ["Dragon attack", "Castle siege", "Bandit ambush", "Quest for a relic", "Royal assassination", "Plague outbreak"],
    "Sci-Fi": ["Alien invasion", "Spaceship malfunction", "Asteroid collision", "Search for a new planet", "Time travel gone wrong", "AI rebellion"],
    "Fantasy": ["Orc raid", "Dark forest adventure", "Cursed artifact", "Rescue mission", "Demon summoning", "Magical tournament"]
}

roles = {
    "Pirate": ["Captain", "Navigator", "Cannoneer", "Swordman", "Cook", "Deckhand", "Quartermaster"],
    "Medieval": ["Knight", "Archer", "Mage", "Healer", "Squire", "Blacksmith", "Monk"],
    "Sci-Fi": ["Commander", "Pilot", "Engineer", "Soldier", "Medic", "Scientist", "AI Specialist"],
    "Fantasy": ["Warrior", "Ranger", "Sorcerer", "Bard", "Alchemist", "Druid", "Thief"]
}

def generate_scenario(genre, num_players):
    situation = random.choice(situations[genre])
    player_roles = random.sample(roles[genre], num_players)
    return situation, player_roles

def generate_background_story(genre, situation, player_roles, player_names):
    prompt = f"You are a Dungeon Master setting up a {genre.lower()} adventure. The players are on the hero's side. The situation is as follows: {situation}. The players are: " + ", ".join([f"{name} as the {role}" for name, role in zip(player_names, player_roles)]) + ". Describe the scene clearly, focusing on the player's perspective and their immediate challenges."
    
    response = model.generate_content(prompt)
    return response.text

def generate_final_story_and_song(genre, situation, player_roles, player_names, player_actions):
    prompt = f"In a {genre} adventure, a group of heroes faced a {situation}. "
    for name, role, action in zip(player_names, player_roles, player_actions):
        prompt += f"{name}, who played the {role}, decided to {action}. "
    prompt += "Describe the outcome of their actions, focusing on their successes and challenges. Conclude with a song inspired by their adventure in an appropriate style. Respond in JSON format with fields 'story', 'song', and 'song_style'."
    
    response = model.generate_content(prompt)
    return response.text

# Example Usage
genre = "Pirate"
num_players = 4
player_names = ["Alice", "Bob", "Charlie", "Diana"]  # Example player names

situation, player_roles = generate_scenario(genre, num_players)
background_story = generate_background_story(genre, situation, player_roles, player_names)

print("Dungeon Master:", background_story)

# Collect player actions
player_actions = []
for name, role in zip(player_names, player_roles):
    action = input(f"What will {name} the {role} do? ")
    player_actions.append(action)

print("Player Actions:", player_actions)

# Generate final output
final_output = generate_final_story_and_song(genre, situation, player_roles, player_names, player_actions)
print("Final Output:", final_output)
