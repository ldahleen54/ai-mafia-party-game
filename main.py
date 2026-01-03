from google import genai
from game_state import game_state
from message_orchestrator import message_orchestrator
import random
from message_sync import message_sync

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
# giving the players the intro
for name in game_state.get_players_alive():
    intro = message_sync.general_intro().replace("(name)", name)
    game_state.chat_history[name] = intro
    if name in game_state.get_doctors_alive():
        game_state.chat_history[name] = game_state.chat_history[name] + "\n\n" + message_sync.doctors_intro()
    elif name in game_state.get_mafia_alive():
        mafia_names = ""        
        for member in game_state.get_mafia_alive():
            mafia_names = mafia_names + member + ", "
        game_state.chat_history[name] = game_state.chat_history[name] + "\n\n" + message_sync.mafia_intro().replace("(names)", mafia_names)
    elif name in game_state.get_detectives_alive():
        game_state.chat_history[name] = game_state.chat_history[name] + "\n\n" + message_sync.detectives_intro()
    else:
        game_state.chat_history[name] = game_state.chat_history[name] + "\n\n" + message_sync.town_intro()

# main game loop
while(game_state.town_won == None):
    if game_state.next_speaker == "":
        print("ERROR Speaker not chosen")
        exit()
    if game_state.time == "night":
        player_message = input(game_state.chat_history[game_state.next_speaker])
        response = message_orchestrator.message(game_state.get_next_speaker(), player_message)
        if "investigated" in response and "is_mafia" in response:
            if response["is_mafia"] == True:
                game_state.chat_history[response["detective"]] = game_state.chat_history[response["detective"]] + "\n\n" + message_sync.confirmed_mafia().replace("(name)", response["investigated"])
            else:
                game_state.chat_history[response["detective"]] = game_state.chat_history[response["detective"]] + "\n\n" + message_sync.not_mafia().replace("(name)", response["investigated"])
    elif game_state.time == "day":
        player_message = input(f"{game_state.chat_history[game_state.next_speaker]} \n\ntime is now day. {game_state.get_next_speaker()}, it is your turn to speak or vote.")
        response = message_orchestrator.message(game_state.get_next_speaker(), player_message)
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