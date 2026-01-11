import random
from prompt import prompt
# Constants
VOTES_RESET = {'Cotton': 0, 'John': 0, 'Samuel': 0, 'William': 0, 'Abigail': 0, 'Ann': 0, 'Betty': 0, 'Sarah': 0, 'Daniel': 0, 'Timothy': 0}
CHAT_HISTORY_RESET = {'Cotton': '', 'John': '', 'Samuel': '', 'William': '', 'Abigail': '', 'Ann': '', 'Betty': '', 'Sarah': '', 'Daniel': '', 'Timothy': ''}

# Globals
chat_history = CHAT_HISTORY_RESET.copy()
players_alive = ["Cotton", "John", "Samuel", "William", "Abigail", "Ann", "Betty", "Sarah", "Daniel", "Timothy"]
speak_forced = {}
players_not_voted = []
day_counter = 0
votes = {}
mafia_members = []
protected_players = []
detectives = []
doctors = []
group_talking = "doctors"
town_won = None
player_killed_last_night = ""
time = "night"
next_speaker = ""
last_protected = ""

def start(total_players, total_mafia, total_detectives, total_doctors):
    if total_players > 10:
        print("ERROR: Total players cannot exceed 10.")
        exit()
    if total_mafia + total_doctors + total_detectives > total_players:
        print("ERROR: Special role count exceeds player count")
        exit()
    players_removed = 10 - total_players
    global players_alive
    players_alive = players_alive[players_removed:]
    player_selection = players_alive.copy()
    #  select the mafia players
    for i in range(total_mafia):
        selected_player = random.choice(player_selection)
        player_selection.remove(selected_player)
        global mafia_members
        mafia_members.append(selected_player)
    # select the detectives
    for i in range(total_detectives):
        selected_player = random.choice(player_selection)
        player_selection.remove(selected_player)
        global detectives
        detectives.append(selected_player)
    # select the doctors
    for i in range(total_doctors):
        selected_player = random.choice(player_selection)
        player_selection.remove(selected_player)
        global doctors
        doctors.append(selected_player)
    # set the votes to 0
    global votes
    votes = VOTES_RESET.copy()
    global chat_history
    chat_history = CHAT_HISTORY_RESET.copy()
    next_night()

# returns boolean whether player is mafia
def lynch_player(name):
    global players_alive
    players_alive.remove(name)
    global votes
    votes = VOTES_RESET.copy()
    next_night()
    global mafia_members
    if name in mafia_members:
        return True
    else:
        return False

# Returns object {"lynch": Boolean, "mafia": Boolean or None, "invalid": Boolean}
def vote_player(voter, name):
    print(f"vote_player ({voter}, {name})")
    global players_not_voted
    if voter not in players_not_voted:
        print(f"Error: Voter {voter} already voted")
        random_speaker()
        return {"lynch": False, "mafia": None, "invalid": True}
    players_not_voted.remove(voter)
    global players_alive
    if name not in players_alive or voter not in players_alive:
        print("Error: Either the voter or name are invalid")
        random_speaker()
        return {"lynch": False, "mafia": None, "invalid": True}
    else:
        global votes
        current_votes = votes[name]
        votes[name] = current_votes + 1
        if votes[name] / len(players_alive) > 0.5:
            # Return whether the player was mafia
            is_mafia = lynch_player(name)
            if is_mafia:
                return {"lynch": True, "mafia": True, "name": name}
            else:
                return {"lynch": True, "mafia": False, "name": name}
        else:
            # allow accused to defend themselves
            if votes[name] == 1:
                defend_next_speaker(name)
            else:
                random_speaker()
            return {"lynch": False, "mafia": None}


# Returns a dictionary
# "error": "message"
# "ended": True
# "ended": False
def mafia_vote_player(voter, name):
    global players_not_voted
    if voter not in players_not_voted:
        print("Error: Player already voted")
        return {"error": "already_voted"}
    global players_alive
    if name not in players_alive:
        print("Error: Player is already dead")
        players_not_voted.remove(voter)
        random_speaker()
        return {"error": "already_dead"}
    players_not_voted.remove(voter)
    global votes
    global current_votes
    current_votes = votes[name]
    votes[name] = votes[name] + 1
    if votes[name] / len(mafia_members) > 0.5:
        attempt = kill_player(name)
        prepare_detectives()
        if attempt == True:
            return {"ended": True, "killed": name}
        else:
            return {"ended": True}
    if len(players_not_voted) <= 0:
        prepare_detectives()
        return {"ended": True}
    else:
        print(f"here are the playes not voted {get_players_not_voted()}")
        global next_speaker
        random_speaker()
        return {"ended": False}

# Returns True if player is killed
# Returns False if player cannot be killed
def kill_player(name):
    global player_killed_last_night
    global protected_players
    player_killed_last_night = ""
    # Make sure the player wasn't protected
    if name not in protected_players:    
        global players_alive
        players_alive.remove(name)
        player_killed_last_night = name
        protected_players = []
        return True
    else:
        protected_players = []
        return False

def next_night():
    print("next night called")
    global votes
    votes = VOTES_RESET.copy()
    global protected_players
    protected_players = []
    global player_killed_last_night
    player_killed_last_night = ""
    global players_not_voted
    players_not_voted = get_mafia_alive().copy()
    global time
    time = "night"
    global speak_forced
    speak_forced = VOTES_RESET.copy()
    prepare_doctors()

def next_day():
    global day_counter
    day_counter = day_counter + 1
    global protected_players
    protected_players = []
    global players_not_voted
    players_not_voted = get_players_alive().copy()
    global votes
    votes = VOTES_RESET.copy()
    global time
    time = "day"
    global town_won
    # Check if mafia won
    if len(get_mafia_alive()) / len(get_players_alive()) >= 0.5:
        town_won = False
    # check if town won
    if len(get_mafia_alive()) <= 0 and len(get_players_alive()) > 0:
        town_won = True
    global speak_forced
    speak_forced = VOTES_RESET.copy()
    global player_killed_last_night
    if player_killed_last_night != "":
        append_chat_all(prompt.daytime_death(player_killed_last_night))
    else:
        append_chat_all(prompt.daytime_no_death())
    random_speaker()

def prepare_doctors():
    print("prepare doctors called")
    global players_not_voted
    players_not_voted = get_doctors_alive()
    global protected_players
    protected_players = []
    global next_speaker
    if len(players_not_voted) <= 0:
        prepare_mafia()
    else:
        global next_speaker
        next_speaker = get_doctors_alive()[0]
        global group_talking
        group_talking = "doctors"

def prepare_mafia():
    global players_not_voted
    players_not_voted = get_mafia_alive()
    global next_speaker
    next_speaker = random.choice(players_not_voted)
    global group_talking
    group_talking = "mafia"

def prepare_detectives():
    global players_not_voted
    players_not_voted = get_detectives_alive()
    global next_speaker
    if len(players_not_voted) > 0:
        next_speaker = players_not_voted[0]
        global group_talking
        group_talking = "detectives"
    else:
        next_day()

def investigate(name, target):
    global players_not_voted
    players_not_voted.remove(name)
    next_day()
    return target in mafia_members

def protect(name, target):
    global last_protected
    if target in get_players_alive() and last_protected != target:
        global protected_players
        protected_players.append(target)
        last_protected = target
    else:
        print("Error: Invalid protection target")
    prepare_mafia()

def random_speaker():
    global next_speaker
    global players_not_voted
    global time
    if len(players_not_voted) > 0:
        new_speaker = next_speaker
        while(new_speaker == next_speaker):
            new_speaker = random.choice(players_not_voted)
        next_speaker = new_speaker
    elif time == "day":
        next_night()
    else:
        prepare_detectives()

# force by using the !speak command
def force_next_speaker(speaker):
    global next_speaker
    global speak_forced
    # player can only be forced to speak twice
    if speaker in get_players_alive() and speak_forced[speaker] < 2:
        next_speaker = speaker
        return
    random_speaker()

def defend_next_speaker(speaker):
    global next_speaker
    if speaker in get_players_alive():
        next_speaker = speaker

def append_chat(name, message):
    global chat_history
    if name in chat_history:
        chat_history[name] = chat_history[name] + "\n\n" + message

def append_chat_all(message):
    global chat_history
    for name in chat_history:
        chat_history[name] = chat_history[name] + "\n\n" + message

def append_chat_except(speaker, message):
    global chat_history
    for name in chat_history:
        if name != speaker:
            chat_history[name] = chat_history[name] + "\n\n" + message

def append_mafia_chat(speaker, message):
    global chat_history
    global mafia_members
    for name in mafia_members:
        if name != speaker:
            append_chat(name, f"{speaker}: " + message)

def clear_chat_all():
    global chat_history
    chat_history = CHAT_HISTORY_RESET.copy()

def clear_chat(name):
    global chat_history
    chat_history[name] = ""

# DEBUG
def debug_info():
    print("DEBUG: Players still alive: ")
    global players_alive
    for name in players_alive:
        print(name)
    print("DEBUG: The mafia members are")
    global mafia_members
    for name in mafia_members:
        print(name)
    print("Debug: Protected players")
    global protected_players
    for name in protected_players:
        print(name)
    print("Debug: Players not voted")
    global players_not_voted
    for name in players_not_voted:
        print(name)
    print("Debug: Votes")
    global votes
    for key in votes:
        print(key)
        print(votes.get(key))
    print(f"DEBUG: Town won? {town_won}.")
    for name in get_doctors_alive():
        print(f"Doctor: {name}")
    global group_talking
    print(f"group_talking: {group_talking}")
    global doctors
    print(f"doctors: {doctors}")
    global detectives
    print(f"detectives: {detectives}")

def debug_add_mafia(name):
    global mafia_members
    mafia_members.append(name)

def debug_clear_mafia():
    global mafia_members
    mafia_members = []
    
# Getters
def get_players_alive():
    global players_alive
    return players_alive

def get_mafia_alive():
    global players_alive
    mafia_members_alive = []
    for name in mafia_members:
        if name in players_alive:
            mafia_members_alive.append(name)
    return mafia_members_alive

def get_players_not_voted():
    global players_not_voted
    return players_not_voted

def get_votes(name):
    global votes
    return votes[name]

def get_time():
    global time
    return time

def get_detectives():
    global detectives
    return detectives

def get_doctors():
    global doctors
    return doctors

def get_doctors_alive():
    doctors_alive = []
    global doctors
    for name in doctors:
        if name in players_alive:
            doctors_alive.append(name)
    return doctors_alive

def get_detectives_alive():
    detectives_alive = []
    global detectives
    for name in detectives:
        if name in players_alive:
            detectives_alive.append(name)
    return detectives_alive

def get_next_speaker():
    global next_speaker
    return next_speaker