import os
import google.generativeai as genai
import random
import json
from fix_busted_json import repair_json

# Configure the generative AI
genai.configure(api_key=os.environ["API_KEY"])


class Game_Model:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-1.5-pro")

        # Define Genres, Roles, and Situations
        self.genres = ["Pirate", "Medieval", "Sci-Fi", "Fantasy"]
        self.roles = {
            "Pirate": ["Captain", "Navigator", "Cannoneer", "Swordman"],
            "Medieval": ["Knight", "Archer", "Mage", "Healer"],
            "Sci-Fi": ["Commander", "Pilot", "Engineer", "Soldier"],
            "Fantasy": ["Warrior", "Ranger", "Sorcerer", "Bard"],
        }

        self.situations = {
            "Pirate": ["Kraken attack", "Enemy ship attack", "Storm", "Treasure hunt"],
            "Medieval": [
                "Dragon attack",
                "Castle siege",
                "Bandit ambush",
                "Quest for a relic",
            ],
            "Sci-Fi": [
                "Alien invasion",
                "Spaceship malfunction",
                "Asteroid collision",
                "Search for a new planet",
            ],
            "Fantasy": [
                "Orc raid",
                "Dark forest adventure",
                "Cursed artifact",
                "Rescue mission",
            ],
        }

    # Generate a random scenario
    def generate_scenario(self, genre, num_players):
        situation = random.choice(self.situations[genre])
        player_roles = random.sample(self.roles[genre], num_players)
        return situation, player_roles

    # Generate the background story with player responsibilities in JSON format
    def generate_background_story(self, genre, situation, player_roles, player_names):
        prompt = (
            f"As the Dungeon Master in a {genre.lower()} setting, a critical situation unfolds: {situation}. "
            f"The party must act swiftly to navigate through the dangers.\n\n"
            "You will generate a JSON object with the following structure:\n\n"
            "{\n"
            '  "prefix_of_general_narration": "[Introduction to the situation that all players see]",\n'
            '  "{Role1}": "[Actionable prompts, responsibilities, and challenges for Player1 in Role1]",\n'
            '  "{Role2}": "[Actionable prompts, responsibilities, and challenges for Player2 in Role2]",\n'
            '  "...": "[Additional roles as needed]",\n'
            '  "suffix_of_general_narration": "[Closing narration that all players see]"\n'
            "}\n\n"
        )

        prompt += "Prefix of the general narration: Describe the scene, setting the tone and the urgency of the situation, which all players will see.\n\n"

        for i, (player_name, role) in enumerate(zip(player_names, player_roles)):
            prompt += (
                f"{role}: The player is {player_name}, and their role is {role}. Provide specific actionable prompts that match their responsibilities in this situation. "
                f"Include at least three responsibilities or actions they must consider:\n"
                f"* **Responsibility 1:** Describe an action that fits the role in the context of the {situation}.\n"
                f"* **Responsibility 2:** Consider the well-being of the group while carrying out their tasks.\n"
                f"* **Responsibility 3:** Evaluate any risks and potential rewards in their actions.\n\n"
            )

        prompt += "Suffix of the general narration: Conclude the setup, emphasizing the urgency and the stakes. This will also be visible to all players.\n\n"

        prompt += "Generate this structured JSON output with the narrations and roles' responsibilities filled in accordingly."

        response = self.model.generate_content(prompt)
        return response.text

    # Generate the final story and song based on player actions
    def generate_final_story_and_song(
        self,
        genre,
        situation,
        player_roles,
        player_names,
        player_actions,
        prefix,
        suffix,
    ):
        prompt = f"In a {genre} adventure, your group of friends faced a {situation}. {prefix} "
        for name, role, action in zip(player_names, player_roles, player_actions):
            prompt += f"{name} ({role}) decided to {action}. "
        prompt += (
            f"{suffix} Write an engaging story about their adventure, including outcomes such as who survived, who got injured, and if they gained anything. "
            "Additionally, create a song inspired by the story in an appropriate style. Respond in JSON format with fields 'story', 'song', and 'song_style'."
        )

        response = self.model.generate_content(prompt)
        return response.text

    def remove_escape_before_single_quote(self, input_str):
        # This regex will match any \' inside double quotes and remove the backslash
        return re.sub(
            r'(?<=")(.*?)(\\\')(.*?)(?=")',
            lambda m: m.group(0).replace("\\'", "'"),
            input_str,
        )

    def get_json_from_text(self, background_story):
        json_start = background_story.find("{")
        json_end = background_story.rfind("}") + 1
        json_string = background_story[json_start:json_end].strip()
        # json_string = self.remove_escape_before_single_quote(json_string)
        json_string = repair_json(json_string)
        try:
            print(repr(json_string))
            print(json_start, json_end)
            print(type(json_string))
            background_story_dict = json.loads(json_string)
        except json.JSONDecodeError as e:
            print("Failed to decode JSON:", e)
            raise

        print(background_story_dict)
        return background_story_dict

    def get_prefix_suffix(self, background_story):
        prefix_narration = ""
        suffix_narration = ""

        try:
            background_story_dict = self.get_json_from_text(
                background_story=background_story
            )

            # Example usage
            prefix_narration = background_story_dict.get(
                "prefix_of_general_narration", ""
            )
            suffix_narration = background_story_dict.get(
                "suffix_of_general_narration", ""
            )
            return prefix_narration, suffix_narration,

        except json.JSONDecodeError as e:
            print("Failed to decode JSON:", e)
        except Exception as e:
            print("An error occurred:", e)

    # Example Usage
    def example(self):
        genre = "Pirate"
        num_players = 4
        player_names = ["Alice", "Bob", "Charlie", "Diana"]
        situation, player_roles = self.generate_scenario(genre, num_players)
        background_story = self.generate_background_story(
            genre, situation, player_roles, player_names
        )

        print("Dungeon Master:", background_story)

        # Example of extracting prefix and suffix from the generated background story (assuming background_story is in JSON format)
        # This part depends on how the JSON is structured when received from the model
        # For example purposes, we'll assume it's a dictionary:
        prefix_narration = ""
        suffix_narration = ""

        try:
            json_start = background_story.find("{")
            json_end = background_story.rfind("}") + 1
            json_string = background_story[json_start:json_end].strip()

            print(json_string)
            # Load the JSON into a dictionary
            background_story_dict = json.loads(json_string)

            # Example usage
            prefix_narration = background_story_dict.get(
                "prefix_of_general_narration", ""
            )
            suffix_narration = background_story_dict.get(
                "suffix_of_general_narration", ""
            )

            print("Prefix Narration:", prefix_narration)
            print("Suffix Narration:", suffix_narration)

        except json.JSONDecodeError as e:
            print("Failed to decode JSON:", e)
        except Exception as e:
            print("An error occurred:", e)

        # Collect player actions
        player_actions = []
        for name, role in zip(player_names, player_roles):
            action = input(f"{name} ({role}), what will you do? ")
            player_actions.append(action)

        print("Player Actions:", player_actions)

        # Generate final output
        final_output = self.generate_final_story_and_song(
            genre,
            situation,
            player_roles,
            player_names,
            player_actions,
            prefix_narration,
            suffix_narration,
        )
        print("Final Output:", final_output)
