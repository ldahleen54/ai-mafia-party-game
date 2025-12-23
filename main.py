from google import genai
import game_state

total_players = 10
total_mafia_members = 3
total_detectives = 1
total_doctors = 1
game_state.start(total_players, total_mafia_members, total_detectives, total_detectives)
game_state.debug_clear_mafia()
game_state.debug_add_mafia("Cotton")
game_state.debug_add_mafia("Ann")
game_state.debug_add_mafia("Samuel")
game_state.debug_info()
game_state.next_night()
game_state.debug_info()
game_state.mafia_vote_player("Cotton", "William")
game_state.mafia_vote_player("Ann", "Sarah")
game_state.mafia_vote_player("Samuel", "Sarah")
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