import os
import google.generativeai as genai


# Configure the generative AI
genai.configure(api_key=os.environ["API_KEY"])

model = genai.GenerativeModel('gemini-1.5-flash')

# Your existing code
import random

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

def generate_scenario(genre, num_players):
    situation = random.choice(situations[genre])
    player_roles = random.sample(roles[genre], num_players)
    return situation, player_roles

def generate_background_story(genre, situation, player_roles):
    prompt = f"Create a background story for a {genre.lower()} adventure. The situation is a {situation}. The roles are: {', '.join(player_roles)}. Narrate the scene as if you are a Dungeon Master, setting up the story for the players."
    
    response = model.generate_content(prompt)
    return response.text

def generate_final_story_and_song(genre, situation, player_roles, player_actions):
    prompt = f"In a {genre} adventure, a group of friends faced a {situation}. "
    for role, action in zip(player_roles, player_actions):
        prompt += f"The {role} decided to {action}. "
    prompt += "Write an interesting story about their adventure, including who survived, who got injured, and if they gained anything. Also, create a song inspired by the story in an appropriate style. Respond in JSON format with fields 'story', 'song', and 'song_style'."
    
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
