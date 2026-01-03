general_intro_file_path = 'prompts/intro.md'
doctor_intro_file_path = 'prompts/doctors.md'
mafia_intro_file_path = 'prompts/mafia.md'
detectives_intro_file_path = 'prompts/detectives.md'
town_intro_file_path = 'prompts/town.md'
confirmed_mafia_file_path = 'prompts/confirmed_mafia.md'
not_mafia_file_path = 'prompts/not_mafia.md'

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

def confirmed_mafia():
    try:
        with open(confirmed_mafia_file_path) as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"Error: The file '{confirmed_mafia_file_path}' was not found.")
    except PermissionError:
        print(f"Error: You do not have permission to read the file '{confirmed_mafia_file_path}'.")
    
def not_mafia():
    try:
        with open(not_mafia_file_path) as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"Error: The file '{not_mafia_file_path}' was not found.")
    except PermissionError:
        print(f"Error: You do not have permission to read the file '{not_mafia_file_path}'.")