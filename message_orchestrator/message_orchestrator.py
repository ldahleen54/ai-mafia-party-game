import random
from game_state import game_state

# Returns None if no command
# Returns {"vote": <name>}
# Returns {"speak": <name>}
# Returns {"investigate": <name>}
# Returns {"protect": <name>}
def parse_commands(message):
    message_list = message.split(" ")
    if "!vote" in message_list:
        vote = message_list.index("!vote")
        if vote + 1 < len(message_list):
            return {"vote": message_list[vote + 1]}
    if "!speak" in message_list:
        speak = message_list.index("!speak")
        if speak + 1 < len(message_list):
            return {"speak": message_list[speak + 1]}
    if "!investigate" in message_list:
        investigate = message_list.index("!investigate")
        if investigate + 1 < len(message_list):
            return {"investigate": message_list[investigate + 1]}
    if "!protect" in message_list:
        protect = message_list.index("!protect")
        if protect + 1 < len(message_list):
            return {"protect": message_list[protect + 1]}
    if "!debug" in message_list:
        game_state.debug_info()

# Returns the result of the commands as a dictionary
# "vote": "name"
# "ended": Boolean
# "error": "message"
# "investigated": {"name": String, "mafia": Boolean}
# "protect": "name"
# only supports one command at a time
def message(name, message):
    commands = parse_commands(message)
    result = {}
    if game_state.get_time() == 'night':
        result = night_commands(name, commands)
    elif game_state.get_time() == 'day':
        result = day_commands(name, commands)
    else:
        print("Error: Invalid time")
    return result
    

# Returns the result of the commands as a dictionary
# "vote": "name"
# "ended": Boolean
# "error": "message"
# "investigated": {"name": String, "mafia": Boolean}
# "protect": "name"
# only supports one command at a time
def night_commands(name, commands):
    result = {}
    if game_state.group_talking == "mafia":
        if commands != None and "vote" in commands:
            target = commands["vote"]
            result = game_state.mafia_vote_player(name, target)
        elif commands != None and "speak" in commands and commands["speak"] in game_state.players_not_voted and game_state.speak_forced[commands["speak"]] < 2:
            game_state.next_speaker = commands["speak"]
            game_state.speak_forced[commands["speak"]] = game_state.speak_forced[commands["speak"]] + 1
        else:
            game_state.next_speaker = random.choice(game_state.get_players_not_voted())
    elif game_state.group_talking == "doctors" and name in game_state.get_doctors():
        # If the doctor doesn't give a valid command just continue
        if commands == None or "protect" not in commands:
            game_state.prepare_mafia()
        else:
            result["protect"] = commands["protect"]
            game_state.protect(name, commands["protect"])
    elif game_state.group_talking == "detectives": 
        if commands != None and "investigate" in commands and name in game_state.get_detectives(): 
            is_mafia = game_state.investigate(name, commands["investigate"])
            result["investigated"] = commands["investigate"]
            result["is_mafia"] = is_mafia
            result["detective"] = name
        else:
            game_state.next_day()
    return result

def day_commands(name, commands):
    result = {}
    if commands != None and "vote" in commands:
        target = commands["vote"]
        result["vote"] = target
        game_state.vote_player(name, target)
    elif commands != None and "speak" in commands and commands["speak"] in game_state.get_players_alive() and commands["speak"] in game_state.get_players_not_voted():
        game_state.next_speaker = commands["speak"]
        game_state.speak_forced[commands["speak"]] = game_state.speak_forced[commands["speak"]] + 1
    else:
        game_state.next_speaker = random.choice(game_state.get_players_not_voted())
    return result
