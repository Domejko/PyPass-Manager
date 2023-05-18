import os
from screeninfo import get_monitors
import re
import hashlib
import string
import random

from dir_cipher import DirectoryCipher


def prefix_generator(pref_len: int) -> str:
    """ Simple function that generates string from alphabet letters and digits 0-9 of length 16
        and returns it. """

    alphabet = list(string.ascii_letters)
    digits = [str(x) for x in range(10)]
    temp = [alphabet, digits]
    prefix = ''
    for _ in range(pref_len):
        prefix += random.choice(random.choice(temp))

    return prefix


def check_os() -> str:
    """ Checks for they type of operating system on which program is running and returns it. """

    if os.name == 'nt':
        return 'Windows'
    else:
        return 'Linux'


def get_user_dir() -> tuple[str, str]:
    """ Checks for the type of operating system on which program is running and returns
    head and tail to user file directory according to user OS. """

    head = os.path.expanduser('~')

    if os.name == 'nt':
        tail = f'/AppData/Local/PM/'
        return head, tail
    else:
        tail = f'/apps/PM/'
        return head, tail


def display_info() -> tuple[float, float]:
    """ Gets information about monitors that a given machine is using, with regex search for a
        main display and save its width and height in a variables. Next check screen resolution
        and according to it's type FHD/QHD/UHD adjust values for GUI to popup in the middle of
        the screen. """

    for m in get_monitors():
        monitor_width = re.search(r'(?<=width=)[0-9]+', str(m)).group()
        monitor_height = re.search(r'(?<=height=)[0-9]+', str(m)).group()
        is_primary = re.search(r'(?<=is_primary=)[a-zA-Z]+', str(m)).group()
        if is_primary == 'True':
            width = int(monitor_width) / 2
            height = int(monitor_height) / 2
            if 2400 < int(monitor_width) < 3000:
                width = width - (700 * 0.625)
                height = height - (450 * 0.625)
            elif int(monitor_width) > 3000:
                width = width - (700 * 0.75)
                height = height - (450 * 0.75)
            else:
                width = width - (700 * 0.50)
                height = height - (450 * 0.50)
            return width, height


def users_list(user_name: str) -> bool:
    """ Search through users_list to avoid creating duplicate users.

    - user_name :            name of a given user """

    head, tail = get_user_dir()
    path = head + tail + f'G4OP28duO04S5r96.bin'

    hash_user = hashlib.sha1(user_name.encode('utf-8')).hexdigest().upper()
    if os.path.isfile(path):
        with open(path, 'r') as users:
            for line in users:
                if hash_user not in line:
                    return False
                else:
                    return True
    else:
        return False


def create_users_list(user_name: str) -> None:
    """ Creates file where usernames are stored.

    - user_name :            name of a given user """

    head, tail = get_user_dir()
    path = head + tail + f'G4OP28duO04S5r96.bin'
    os.makedirs(os.path.dirname(path), exist_ok=True)

    hash_user = hashlib.sha1(user_name.encode('utf-8')).hexdigest().upper()
    if not os.path.exists(path):
        with open(path, 'w') as users:
            users.write(hash_user + '\n')
    with open(path, 'r+') as users:
        users.write(hash_user + '\n')


def fetch_directions_paths(user_name: str, password: str) -> bool | tuple[bytes, bytes, bytes]:
    """ Function that first hashes a username with password and then accordingly to a current
    OS go to a fixed directory where file with a directories dictionaries is stored. Compare a
    hashed username with previously stored hashes, as it finds match it decrypt key_path with a key
    from encoded part of hashed password and returns the paths.

    - user_name :            login of a given user \n
    - password :             password to that given site/thing that will be stored with it """

    hash_password = hashlib.sha3_512(password.encode('utf-8')).hexdigest()
    hash_user = hashlib.sha1(user_name.encode('utf-8')).hexdigest().upper()
    binary_key = hash_password[20:52].encode()
    file_name = hash_user[:16]
    head, tail = get_user_dir()

    if not os.path.exists(f'{head}{tail}{file_name}.bin'):
        return False

    with open(f'{head}{tail}{file_name}.bin', 'r') as login_paths:
        for line in login_paths:
            path = eval(line)
            if path['####1'] == hash_user:
                key_path = DirectoryCipher(binary_key).decrypt_directory(path['####2'])
                login_path = DirectoryCipher(binary_key).decrypt_directory(path['####3'])
                site_path = DirectoryCipher(binary_key).decrypt_directory(path['####4'])
                return key_path, login_path, site_path
    return False


def store_direction_paths(user_user: str, key_path: str, login_path: str, site_path: str, hash_password: str) -> None:
    """ Function that takes username with files paths and create a directory (accordingly
    to OS of device) where file paths are encrypted by a 32 byte key and together with hashed
    username are saved to a file in a form of a dictionary.

    - user_name :            login to a new account \n
    - key_path :             path where user key is stored \n
    - login_path :           path where user account name with password are stored \n
    - site_path :            path where a give account passwords are stored """

    hash_user = hashlib.sha1(user_user.encode('utf-8')).hexdigest().upper()
    binary_key = hash_password[20:52].encode()
    file_name = hash_user[:16]
    encrypted_key_path = DirectoryCipher(binary_key).encrypt_directory(key_path.encode(), file_name.encode())
    encrypted_login_path = DirectoryCipher(binary_key).encrypt_directory(login_path.encode(), file_name.encode())
    encrypted_site_path = DirectoryCipher(binary_key).encrypt_directory(site_path.encode(), file_name.encode())

    direction_dict = {'####1': hash_user,
                      '####2': encrypted_key_path,
                      '####3': encrypted_login_path,
                      '####4': encrypted_site_path}

    head, tail = get_user_dir()
    path = head + tail + f'{file_name}.bin'
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, 'a') as data:
        data.write(str(direction_dict) + "\n")


def delete_files(user_name: str, password: str) -> None:
    """ Deletes all files associated with a given user account.

    - user_name :                 name of a given user account \n
    - password :             password to that account """

    hash_user = hashlib.sha1(user_name.encode('utf-8')).hexdigest().upper()
    file_name = hash_user[:16]
    head, tail = get_user_dir()
    dir_p = head + tail + f'{file_name}.bin'

    key_p, login_p, site_p = fetch_directions_paths(user_name, password)
    os.remove(key_p)
    os.remove(login_p)
    os.remove(site_p)
    os.remove(dir_p)

    path = head + tail + f'G4OP28duO04S5r96.bin'

    with open(path, 'r') as users:
        lines = users.readlines()

    with open(path, 'w') as users:
        for line in lines:
            if line.strip("\n") != hash_user:
                users.write(line)
