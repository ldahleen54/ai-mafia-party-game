from google import genai
import game_state

total_players = 10
total_mafia_members = 3
total_detectives = 1
total_doctors = 1
game_state.start(total_players, total_mafia_members, total_detectives, total_detectives)
game_state.debug_info()
game_state.lynch_player("Cotton")
game_state.debug_info()
game_state.protect_player("Betty")
game_state.kill_player("Betty")
game_state.debug_info()
game_state.vote_player("Abigail")
game_state.debug_info



# client = genai.Client()

# response = client.models.generate_content(
#     model="gemini-3-flash-preview",
#     config=types.GenerateContentConfig(
#         system_instruction=""
#     )
#     contents="Explain how AI works in a few words",
# )

# print(response.text)