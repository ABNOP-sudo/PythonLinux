import os
import readline
import time
import sys
import getpass
import json
import random
import string

PASSWORD_FILE = "Password.txt"
DEBUG_LOG = "debug.log"
USER_FS_FILE = "user_fs.json"

def log_debug(message):
    with open(DEBUG_LOG, "a") as log_file:
        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

def load_passwords():
    if not os.path.exists(PASSWORD_FILE):
        return {}
    with open(PASSWORD_FILE, "r") as f:
        lines = f.read().splitlines()
        return dict(line.split(":") for line in lines if ":" in line)

def save_password(username, password):
    with open(PASSWORD_FILE, "a") as f:
        f.write(f"{username}:{password}\n")

def load_all_fs():
    if os.path.exists(USER_FS_FILE):
        with open(USER_FS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_all_fs():
    with open(USER_FS_FILE, "w") as f:
        json.dump(all_fs, f, indent=4)

def load_user_fs(username):
    return all_fs.get(username, create_new_fs(username))

def save_user_fs(username):
    all_fs[username] = fake_fs
    save_all_fs()

def create_new_fs(username):
    return {
        "home": {username: {}},
        "root": {"secure.txt": "Секретные данные!"},
        "etc": {},
        "var": {},
        "bin": {},
        "usr": {},
        "tmp": {},
        "dev": {},
        "proc": {},
        "sys": {}
    }

def get_dir(path):
    parts = path.strip("/").split("/")
    current = fake_fs
    for part in parts:
        if part:
            if part in current:
                current = current[part]
            else:
                return None
    return current

def random_dir_name():
    return "".join(random.choices(string.ascii_lowercase, k=random.randint(3, 6)))

def generate_virus_game():
    directories = [random_dir_name() for _ in range(random.randint(3, 6))]
    game_fs = {name: {} for name in directories}
    virus_dir = random.choice(directories)
    game_fs[virus_dir]["virus.exe"] = "Опасный вирус! Удали его командой `rm virus.exe`"
    return game_fs, virus_dir

def boot_sequence():
    messages = [
        "[    0.000000] Booting Linux kernel 5.10.0-21-amd64...",
        "[    0.002345] Initializing system...",
        "[    0.005678] Loading kernel modules...",
        "[    0.010000] Mounting file systems...",
        "[    0.015432] Starting system services...",
        "[    0.020123] Checking disk integrity... OK",
        "[    0.025678] Network interfaces initializing... OK",
        "[    0.030789] Running system diagnostics... OK",
        "[    0.035678] Launching user session..."
    ]
    for msg in messages:
        print(msg)
        time.sleep(0.2)
    print("\nWelcome to Debian!")
    log_debug("System boot completed.")

def shell():
    global current_path, fake_fs, username, all_fs

    while True:
        prompt = "$"
        print_path = current_path.rstrip("/") if current_path != "/" else "/"
        cmd = input(f"{username}@debian:{print_path}{prompt} ").strip().split()
        
        if not cmd:
            continue
        
        command, *args = cmd
        log_debug(f"Command executed: {command} {' '.join(args)}")
        
        try:
            if command == "exit":
                print("Выход...")
                if username != "Virus":
                    save_user_fs(username)
                log_debug("User exited shell.")
                break

            elif command == "logout":
                print("Выход из системы...")
                if username != "Virus":
                    save_user_fs(username)
                login()
                break

            elif command == "ls":
                dir_content = get_dir(current_path)
                print(" ".join(dir_content.keys()) if dir_content else "(пусто)")

            elif command == "cd":
                if args:
                    new_path = args[0]
                    potential_path = get_dir(f"{current_path}/{new_path}".replace("//", "/"))
                    if new_path == "..":
                        if current_path != "/":
                            current_path = "/".join(current_path.rstrip("/").split("/")[:-1]) or "/"
                    elif potential_path is not None and isinstance(potential_path, dict):
                        current_path = f"{current_path}/{new_path}".replace("//", "/")
                    else:
                        print("Папка не найдена")

            elif command == "rm":
                if args:
                    dir_content = get_dir(current_path)
                    if args[0] in dir_content:
                        del dir_content[args[0]]

                        if username != "Virus":
                            save_user_fs(username)

                        print(f"Удалено: {args[0]}")

                        if username == "Virus" and args[0] == "virus.exe":
                            print("🎉 Ты победил! Вирус удалён! 🎉")
                            break
                    else:
                        print("Файл не найден")

            elif command == "mkdir":
                if args:
                    dir_name = args[0]
                    dir_content = get_dir(current_path)
                    if isinstance(dir_content, dict):
                        dir_content[dir_name] = {}
                        if username != "Virus":
                            save_user_fs(username)
                        print(f"Папка '{dir_name}' создана")

            elif command == "touch":
                if args:
                    file_name = args[0]
                    dir_content = get_dir(current_path)
                    if isinstance(dir_content, dict):
                        dir_content[file_name] = ""
                        if username != "Virus":
                            save_user_fs(username)
                        print(f"Файл '{file_name}' создан")

            elif command == "cat":
                if args:
                    file_name = args[0]
                    dir_content = get_dir(current_path)
                    if file_name in dir_content:
                        print(dir_content[file_name])
                    else:
                        print("Файл не найден")

            elif command == "clear":
                os.system("cls" if os.name == "nt" else "clear")

            elif command == "help":
                print("Available commands:")
                print("  ls       - List files and directories")
                print("  cd       - Change directory")
                print("  mkdir    - Create a new directory")
                print("  touch    - Create a new file")
                print("  cat      - Read a file")
                print("  rm       - Remove a file or directory")
                print("  clear    - Clear the terminal")
                print("  logout   - Logout and switch user")
                print("  exit     - Exit the shell")

            else:
                print(f"Команда '{command}' не найдена")
        except Exception as e:
            log_debug(f"Error executing command {command}: {str(e)}")
            print(f"Ошибка при выполнении команды: {e}")
def virus_game():
    global current_path, fake_fs, username
    print(r"""
 ██▒   █▓ ██▓ ██▀███   █    ██   ██████      ▄████  ▄▄▄       ███▄ ▄███▓▓█████ 
▓██░   █▒▓██▒▓██ ▒ ██▒ ██  ▓██▒▒██    ▒     ██▒ ▀█▒▒████▄    ▓██▒▀█▀ ██▒▓█   ▀ 
 ▓██  █▒░▒██▒▓██ ░▄█ ▒▓██  ▒██░░ ▓██▄      ▒██░▄▄▄░▒██  ▀█▄  ▓██    ▓██░▒███   
  ▒██ █░░░██░▒██▀▀█▄  ▓▓█  ░██░  ▒   ██▒   ░▓█  ██▓░██▄▄▄▄██ ▒██    ▒██ ▒▓█  ▄ 
   ▒▀█░  ░██░░██▓ ▒██▒▒▒█████▓ ▒██████▒▒   ░▒▓███▀▒ ▓█   ▓██▒▒██▒   ░██▒░▒████▒
   ░ ▐░  ░▓  ░ ▒▓ ░▒▓░░▒▓▒ ▒ ▒ ▒ ▒▓▒ ▒ ░    ░▒   ▒  ▒▒   ▓▒█░░ ▒░   ░  ░░░ ▒░ ░
   ░ ░░   ▒ ░  ░▒ ░ ▒░░░▒░ ░ ░ ░ ░▒  ░ ░     ░   ░   ▒   ▒▒ ░░  ░      ░ ░ ░  ░
     ░░   ▒ ░  ░░   ░  ░░░ ░ ░ ░  ░  ░     ░ ░   ░   ░   ▒   ░      ░      ░   
      ░   ░     ░        ░           ░           ░       ░  ░       ░      ░  ░
     ░                                                                         
""")

    fake_fs, _ = generate_virus_game()
    current_path = "/"
    print("Вирус спрятан. Найди его и удали `rm virus.exe`!\n")
    shell()

def login():
    global username, current_path, fake_fs, all_fs
    passwords = load_passwords()
    username = input("Введите имя пользователя: ")
    
    if username == "Virus":
        password = getpass.getpass("Введите пароль: ")
        if password == "Game":
            virus_game()
            return
    
    if username in passwords:
        while True:
            password = getpass.getpass("Введите пароль: ")
            if password == passwords[username]:
                print("Аутентификация успешна. Добро пожаловать!")
                break
            else:
                print("Неверный пароль! Попробуйте снова.")
    else:
        print("Новый пользователь. Создайте пароль.")
        password = getpass.getpass("Введите новый пароль: ")
        save_password(username, password)
        print("Пользователь зарегистрирован!")
    
    all_fs = load_all_fs()
    fake_fs = load_user_fs(username)
    if "home" not in fake_fs:
        fake_fs["home"] = {}
    if username not in fake_fs["home"]:
        fake_fs["home"][username] = {}
    current_path = f"/home/{username}"
    
    print("Type 'help' for a list of available commands.")
    shell()

if __name__ == "__main__":
    boot_sequence()
    login()
