import json
import platform
import subprocess

def copy_to_clipboard(text):
    system = platform.system()

    try:
        if system == "Linux":
            # Пробуем xclip, затем xsel, затем wl-clipboard
            for cmd in [['xclip', '-selection', 'clipboard'],
                        ['xsel', '--clipboard', '--input'],
                        ['wl-copy']]:
                try:
                    subprocess.run(cmd, input=text, text=True, check=True,
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    return True
                except (subprocess.SubprocessError, FileNotFoundError):
                    continue
            return False

        elif system == "Windows":
            subprocess.run(['clip'], input=text, text=True, check=True)
            return True

        elif system == "Darwin":  # macOS
            subprocess.run(['pbcopy'], input=text, text=True, check=True)
            return True

    except Exception:
        pass

    return False

def read_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def read_name(data):
    names = list(data.keys())
    while True:
        name = input("Enter name of JetBrains IDE: ").lower()
        if name in [key.lower() for key in names]:
            return name
        else:
            show_list = input("Incorrect name! Show list of IDEs? [y/n]: ")
            if show_list == 'y':
                print(*names, sep='\n')


if __name__ == '__main__':
    data = read_json("keys.json")
    name = read_name(data)
    data = {key.lower(): value for key, value in data.items()}
    ide = data[name]
    if copy_to_clipboard(str(*ide.values())):
        print("Key for version", *ide.keys(), "successfully copied to clipboard")
    else:
        print("Copying key for version", *ide.keys(), "to clipboard failed. Copy manually.\n\n", *ide.values())




