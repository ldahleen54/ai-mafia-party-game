from google import genai
from game_state import game_state
from message_orchestrator import message_orchestrator
import random

total_players = 10
total_mafia_members = 3
total_detectives = 1
total_doctors = 1
game_state.start(total_players, total_mafia_members, total_detectives, total_detectives)
game_state.debug_clear_mafia()
game_state.debug_add_mafia("Cotton")
game_state.debug_add_mafia("Ann")
game_state.debug_add_mafia("Samuel")
game_state.next_night()
while(game_state.town_won == None):
    if game_state.next_speaker == "":
        print("ERROR Speaker not chosen")
        exit()
    if game_state.time == "night":
        if game_state.group_talking == "doctors":
            player_message = input(f"hello you are the doctor it is your turn to speak {game_state.get_next_speaker()}")
        elif game_state.group_talking == "mafia":
            player_message = input(f"hello you are a member of the mafia it is your turn to speak {game_state.get_next_speaker()}")
        elif game_state.group_talking == "detectives":
            player_message = input(f"hello you are the detective it is your turn to speak {game_state.get_next_speaker()}")
        response = message_orchestrator.message(game_state.get_next_speaker(), player_message)
        if "investigated" in response:
            print(f"investigated: {response["investigated"]}")
    elif game_state.time == "day":
        player_message = input(f"time is now day. {game_state.get_next_speaker()}, it is your turn to speak or vote.")
        response = message_orchestrator.message(game_state.get_next_speaker(), player_message)
game_state.debug_info()

# client = genai.Client()

# response = client.models.generate_content(
#     model="gemini-3-flash-preview",
#     config=types.GenerateContentConfig(
#         system_instruction=""
#     )
#     contents="Explain how AI works in a few words",
# )

# print(response.text)