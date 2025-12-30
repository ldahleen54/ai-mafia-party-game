import random
VOTES_RESET = {'Cotton': 0, 'John': 0, 'Samuel': 0, 'William': 0, 'Abigail': 0, 'Ann': 0, 'Betty': 0, 'Sarah': 0, 'Daniel': 0, 'Timothy': 0}
CHAT_HISTORY_RESET = {'Cotton': '', 'John': '', 'Samuel': '', 'William': '', 'Abigail': '', 'Ann': '', 'Betty': '', 'Sarah': '', 'Daniel': '', 'Timothy': ''}
chat_history = {}
players_alive = ["Cotton", "John", "Samuel", "William", "Abigail", "Ann", "Betty", "Sarah", "Daniel", "Timothy"]
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
    votes = VOTES_RESET
    global chat_history
    chat_history = CHAT_HISTORY_RESET
    next_night()
    prepare_doctors()

# returns boolean whether player is mafia
def lynch_player(name):
    global players_alive
    players_alive.remove(name)
    votes = VOTES_RESET
    if name in get_mafia_alive():
        return True
    else:
        return False

# Returns object {"lynch": Boolean, "mafia": Boolean or None, "invalid": Boolean}
def vote_player(voter, name):
    if voter not in players_not_voted:
        print(f"Error: Voter {voter} already voted")
        return {"lynch": False, "mafia": None, "invalid": True}
    players_not_voted.remove(voter)
    if name not in players_alive:
        print("Error: Player name is invalid")
        return {"lynch": False, "mafia": None, "invalid": True}
    else:
        global votes
        current_votes = votes[name]
        votes[name] = current_votes + 1
        if votes[name] / len(players_alive) > 0.5:
            # Return whether the player was mafia
            is_mafia = lynch_player(name)
            if is_mafia:
                return {"lynch": True, "mafia": True}
            else:
                return {"lynch": True, "mafia": False}
        else:
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
        next_speaker = random.choice(get_players_not_voted())
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
    global votes
    votes = VOTES_RESET
    global protected_players
    protected_players = []
    global player_killed_last_night
    player_killed_last_night = ""
    global players_not_voted
    players_not_voted = get_mafia_alive().copy()
    global time
    time = "night"

def next_day():
    global day_counter
    day_counter = day_counter + 1
    global protected_players
    protected_players = []
    global players_not_voted
    players_not_voted = get_players_alive()
    global votes
    votes = VOTES_RESET
    global time
    time = "day"
    global town_won
    # Check if mafia won
    if len(get_mafia_alive()) / len(get_players_alive()) >= 0.5:
        town_won = False
    # check if town won
    if len(get_mafia_alive()) <= 0 and len(get_players_alive()) > 0:
        town_won = True

def prepare_doctors():
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
    if len(players_not_voted) >= 0:
        next_speaker = players_not_voted[0]
    global group_talking
    group_talking = "detectives"


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

# DEBUG
def debug_info():
    print("DEBUG: Players still alive: ")
    for name in players_alive:
        print(name)
    print("DEBUG: The mafia members are")
    for name in mafia_members:
        print(name)
    print("Debug: Protected players")
    for name in protected_players:
        print(name)
    print("Debug: Players not voted")
    for name in players_not_voted:
        print(name)
    print("Debug: Votes")
    for key in votes:
        print(key)
        print(votes.get(key))
    print(f"DEBUG: Town won? {town_won}.")
    for name in get_doctors_alive():
        print(f"Doctor: {name}")
    global group_talking
    print(f"group_talking: {group_talking}")
    global doctors
    print(doctors)

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