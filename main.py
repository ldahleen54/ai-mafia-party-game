from google import genai
from game_state import game_state
from message_orchestrator import message_orchestrator
import random
from prompt import prompt

# configs
total_players = 10
total_mafia_members = 3
total_detectives = 1
total_doctors = 1

game_state.start(total_players, total_mafia_members, total_detectives, total_detectives)

# Debug commands
game_state.debug_clear_mafia()
game_state.debug_add_mafia("Cotton")
game_state.debug_add_mafia("Ann")
game_state.debug_add_mafia("Samuel")
# give every player the introduction and game instructions

for name in game_state.get_players_alive():
    game_state.append_chat(name, prompt.general_intro().replace("(name)", name))
    if name in game_state.get_doctors_alive():
        game_state.append_chat(name, prompt.doctors_intro())
    elif name in game_state.get_mafia_alive():
        mafia_names = ""        
        for member in game_state.get_mafia_alive():
            mafia_names = mafia_names + member + ", "
        game_state.append_chat(name, prompt.mafia_intro().replace("(names)", mafia_names))
    elif name in game_state.get_detectives_alive():
        game_state.append_chat(name, prompt.detectives_intro())
    else:
        game_state.append_chat(name, prompt.town_intro())
# main game loop
while(game_state.town_won == None):
    if game_state.next_speaker == "":
        print("ERROR Speaker not chosen")
        exit()
    current_speaker = game_state.next_speaker
    if game_state.time == "night":
        game_state.append_chat(current_speaker, prompt.your_turn(current_speaker))
        player_message = input(game_state.chat_history[current_speaker])
        game_state.clear_chat(current_speaker)
        response = message_orchestrator.message(current_speaker, player_message)
        if "investigated" in response and "is_mafia" in response:
            if response["is_mafia"] == True:
                game_state.append_chat(current_speaker, prompt.confirmed_mafia(response["investigated"]))
            else:
                game_state.append_chat(current_speaker, prompt.not_mafia(response["investigated"]))
    elif game_state.time == "day":
        game_state.append_chat(current_speaker, prompt.your_turn(current_speaker))
        player_message = input(game_state.chat_history[current_speaker])
        game_state.clear_chat(current_speaker)
        response = message_orchestrator.message(current_speaker, player_message)
        if "lynch" in response and response["lynch"] == True:
            print(f"{response["name"]} has been lynched")
            if response["mafia"] == True:
                print(f"Moderator: {response["name"]} was mafia")
            else:
                print(f"Moderator: {response["name"]} was not mafia")

# client = genai.Client()

# response = client.models.generate_content(
#     model="gemini-3-flash-preview",
#     config=types.GenerateContentConfig(
#         system_instruction=""
#     )
#     contents="Explain how AI works in a few words",
# )

# print(response.text)