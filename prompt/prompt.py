general_intro_file_path = 'prompts/intro.md'
doctor_intro_file_path = 'prompts/doctors.md'
mafia_intro_file_path = 'prompts/mafia.md'
detectives_intro_file_path = 'prompts/detectives.md'
town_intro_file_path = 'prompts/town.md'
confirmed_mafia_file_path = 'prompts/confirmed_mafia.md'
not_mafia_file_path = 'prompts/not_mafia.md'
daytime_death_file_path = 'prompts/daytime_death.md'
daytime_no_death_file_path = 'prompts/daytime_no_death.md'
your_turn_file_path = 'prompts/your_turn.md'

def general_intro():
    try:
        with open(general_intro_file_path) as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"Error: The file '{general_intro_file_path}' was not found.")
    except PermissionError:
        print(f"Error: You do not have permission to read the file '{general_intro_file_path}'.")

def doctors_intro():
    try:
        with open(doctor_intro_file_path) as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"Error: The file '{doctor_intro_file_path}' was not found.")
    except PermissionError:
        print(f"Error: You do not have permission to read the file '{doctor_intro_file_path}'.")

def mafia_intro():
    try:
        with open(mafia_intro_file_path) as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"Error: The file '{mafia_intro_file_path}' was not found.")
    except PermissionError:
        print(f"Error: You do not have permission to read the file '{mafia_intro_file_path}'.")

def detectives_intro():
    try:
        with open(detectives_intro_file_path) as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"Error: The file '{detectives_intro_file_path}' was not found.")
    except PermissionError:
        print(f"Error: You do not have permission to read the file '{detectives_intro_file_path}'.")

def town_intro():
    try:
        with open(town_intro_file_path) as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"Error: The file '{town_intro_file_path}' was not found.")
    except PermissionError:
        print(f"Error: You do not have permission to read the file '{town_intro_file_path}'.")

def confirmed_mafia(name):
    try:
        with open(confirmed_mafia_file_path) as file:
            content = file.read()
            return content.replace("(name)", name)
    except FileNotFoundError:
        print(f"Error: The file '{confirmed_mafia_file_path}' was not found.")
    except PermissionError:
        print(f"Error: You do not have permission to read the file '{confirmed_mafia_file_path}'.")
    
def not_mafia(name):
    try:
        with open(not_mafia_file_path) as file:
            content = file.read()
            return content.replace("(name)", name)
    except FileNotFoundError:
        print(f"Error: The file '{not_mafia_file_path}' was not found.")
    except PermissionError:
        print(f"Error: You do not have permission to read the file '{not_mafia_file_path}'.")

def daytime_death(name):
    try:
        with open(daytime_death_file_path) as file:
            content = file.read()
            return content.replace("(name)", name)
    except FileNotFoundError:
        print(f"Error: The file '{daytime_death_file_path}' was not found.")
    except PermissionError:
        print(f"Error: You do not have permission to read the file '{daytime_death_file_path}'.")

def daytime_no_death():
    try:
        with open(daytime_no_death_file_path) as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"Error: The file '{daytime_no_death_file_path}' was not found.")
    except PermissionError:
        print(f"Error: You do not have permission to read the file '{daytime_no_death_file_path}'.")

def your_turn(name):
    try:
        with open(your_turn_file_path) as file:
            content = file.read()
            return content.replace("(name)", name)
    except FileNotFoundError:
        print(f"Error: The file '{your_turn_file_path}' was not found.")
    except PermissionError:
        print(f"Error: You do not have permission to read the file '{your_turn_file_path}'.")