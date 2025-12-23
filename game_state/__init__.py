import random

players_alive = ["Cotton", "John", "Samuel", "William", "Abigail", "Ann", "Betty", "Sarah", "Daniel", "Timothy"]
votes = {}
mafia_members = []
protected_players = []
town_won = False
player_killed_last_night = ""

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
    votes = {'Cotton': 0, 'John': 0, 'Samuel': 0, 'William': 0, 'Abigail': 0, 'Ann': 0, 'Betty': 0, 'Sarah': 0, 'Daniel': 0, 'Timothy': 0}

# returns boolean whether player is mafia
def lynch_player(name):
    global players_alive
    players_alive.remove(name)
    if name in mafia_members:
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

def vote_player(name):
    if name not in players_alive:
        print("Error: Player name is invalid")
        return False
    else:
        global votes
        current_votes = votes[name]
        votes[name] = current_votes + 1
        return True
    

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
    print("Debug: Votes")
    for key in votes:
        print(key)
        print(votes.get(key))
    print(f"DEBUG: Town winning? {town_won}.")
    
def get_players_alive():
    return players_alive

def get_mafia_alive():
    mafia_members_alive = []
    for name in mafia_members:
        if name in players_alive:
            mafia_members_alive.append(name)
    return mafia_members_alive