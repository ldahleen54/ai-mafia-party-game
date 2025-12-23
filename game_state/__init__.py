import random
VOTES_RESET = {'Cotton': 0, 'John': 0, 'Samuel': 0, 'William': 0, 'Abigail': 0, 'Ann': 0, 'Betty': 0, 'Sarah': 0, 'Daniel': 0, 'Timothy': 0} 
players_alive = ["Cotton", "John", "Samuel", "William", "Abigail", "Ann", "Betty", "Sarah", "Daniel", "Timothy"]
players_not_voted = []
day_counter = 1
votes = {}
mafia_members = []
protected_players = []
town_won = None
player_killed_last_night = ""
time = "night"

def start(total_players, total_mafia, total_detectives, total_doctors):
    if total_players > 10:
        print("ERROR: Total players cannot exceed 10.")
        exit()
    players_removed = 10 - total_players
    global players_alive
    players_alive = players_alive[players_removed:]
    player_selection = players_alive.copy()
    for i in range(total_mafia):
        selected_player = random.choice(player_selection)
        player_selection.remove(selected_player)
        global mafia_members
        mafia_members.append(selected_player)
    # set the votes to 0
    global votes
    votes = VOTES_RESET

# returns boolean whether player is mafia
def lynch_player(name):
    global players_alive
    players_alive.remove(name)
    votes = VOTES_RESET
    if name in get_mafia_alive():
        return True
    else:
        return False

def protect_player(name):
    # Check if player name is valid
    if name not in players_alive:
        print("Error: Player name is invalid")
        return False
    else:
        protected_players.append(name)
        return True

# Returns object {"lynch": Boolean, "mafia": Boolean or None, "invalid": Boolean}
def vote_player(voter, name):
    players_not_voted.append(voter)
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

# Returns True when voting is over
def mafia_vote_player(voter, name):
    if voter not in players_not_voted:
        print("Error: Player already voted")
        return False
    if name not in players_alive:
        print("Error: Player is already dead")
        return False
    players_not_voted.remove(voter)
    current_votes = votes[name]
    votes[name] = votes[name] + 1
    if votes[name] / len(mafia_members) > 0.5:
        kill_player(name)
        return True
    if len(players_not_voted) <= 0:
        return True
    return False

# mafia or vigilante tries to kill this player
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

def next_night():
    global votes
    votes = VOTES_RESET
    global protected_players
    protected_players = []
    global player_killed_last_night
    player_killed_last_night = ""
    global players_not_voted
    players_not_voted = get_mafia_alive()
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
    if len(get_mafia_alive()) / len(get_players_alive) >= 0.5:
        town_won = False
    # check if town won
    if len(get_mafia_alive) <= 0 and len(get_players_alive) > 0:
        town_won = True

def investigate(name):
    return name in mafia_members

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
    print("Debug:Players not voted")
    for name in players_not_voted:
        print(name)
    print("Debug: Votes")
    for key in votes:
        print(key)
        print(votes.get(key))
    print(f"DEBUG: Town won? {town_won}.")

def debug_add_mafia(name):
    global mafia_members
    mafia_members.append(name)

def debug_clear_mafia():
    global mafia_members
    mafia_members = []
    
# Getters
def get_players_alive():
    return players_alive

def get_mafia_alive():
    mafia_members_alive = []
    for name in mafia_members:
        if name in players_alive:
            mafia_members_alive.append(name)
    return mafia_members_alive

def get_players_not_voted():
    return players_not_voted

def get_votes(name):
    return votes[name]