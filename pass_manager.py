from typing import Type
from cryptography.fernet import Fernet
import os
import hashlib

from tools import users_list, store_direction_paths, prefix_generator, get_user_dir, create_users_list


class PasswordManager:
    def __init__(self) -> None:
        self.key = None
        self.password_file = None
        self.password_dict = {}

    def create_key(self, key_path: str) -> bool:
        """ Generate binary key for a given account.

        - key_path:         directory of where they file will be stored """

        self.key = Fernet.generate_key()

        try:
            with open(key_path, 'wb') as key_file:
                key_file.write(self.key)
                return True
        except PermissionError:
            return False

    def create_password_file(self, path: str, key_path: str, initial_values: dict = None) -> None:
        """ Create a file where hashed users passwords will be stored passing further information
        that will be hashed and saved in created file.

         - site_path:       directory of where uses password will be stored \n
         - key_path:        direction of where user key will be stored \n
         - initial_values:  dictionary containing specific account login and password """

        self.password_file = path

        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb'):
            pass

        if initial_values is not None:
            for user, password in initial_values.items():
                self.add_password(user, password, key_path, path)

    def create_new_user(self, user_name: str, password: str, key_file_path: str) -> Type[PermissionError] | bool:
        """ Checks for duplicate account names. \n
        Prepare new paths variables which are further passed to another functions/methods that create
        directories and files for new user. \n
        Prepare given new user information and passing them to another functions/methods for further
        processing.

        - user_name :        login of a give new user \n
        - password :         password to account of a give new user \n
        - file_path :        directory selected by a user where those files will be created """

        if users_list(user_name):
            return False

        head, tail = get_user_dir()
        user_dict = {user_name: password}
        hashed = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

        new_key_path = key_file_path + f'/{prefix_generator(16)}.bin'
        new_user_path = head + tail + f'/{prefix_generator(16)}.bin'
        new_sites_path = head + tail + f'/{prefix_generator(16)}.bin'

        if os.path.isfile(new_key_path) or os.path.isfile(new_user_path) or os.path.isfile(new_sites_path):
            new_key_path = key_file_path + f'/{prefix_generator(24)}.bin'
            new_user_path = head + tail + f'/{prefix_generator(24)}.bin'
            new_sites_path = head + tail + f'/{prefix_generator(24)}.bin'

        if self.create_key(new_key_path):
            self.create_password_file(new_user_path, new_key_path, user_dict)

            with open(new_sites_path, 'wb'):
                pass

            store_direction_paths(user_name, new_key_path, new_user_path, new_sites_path, hashed)
            create_users_list(user_name)
            return True

        else:
            return PermissionError

    def load_password_file(self, path: str) -> None:
        """ Loads a file from a given path where encrypted passwords are stored and with a give
        key decrypt them and save in a variable.

        - path:             path with a file containing passwords to account or sites """

        self.password_file = path

        with open(path, 'r') as file:
            for line in file:
                try:
                    site, encrypted = line.split(":")
                    site = Fernet(self.key).decrypt(site.encode()).decode()
                    self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()
                except ValueError:
                    continue

    def add_password(self, site: str, password: str, key_path: str, site_path: str) -> None:
        """ With a specific key unique to every account this method opens a path where given user
        passwords are stored and with that specific key encrypts passwords and add them to a file.

        - site:             website or name to any given thing to which password will be assigned \n
        - password:         password to that given site/thing that will be stored with it \n
        - key_path:         path to where user key file is stored \n
        - site_path:        path to where users sites passwords file is stored """

        with open(key_path, 'rb') as file:
            self.key = file.readline()

        self.load_password_file(site_path)
        self.password_dict[site] = password

        if self.password_file is not None:
            with open(self.password_file, 'a+') as file:
                encrypted_login = Fernet(self.key).encrypt(site.encode())
                encrypted_password = Fernet(self.key).encrypt(password.encode())
                file.write(encrypted_login.decode() + ':' + encrypted_password.decode() + '\n')

    def get_pass(self, key_path: str, path: str, site: str) -> str:
        """ With a give key path it's storing key value to a variable and passing site_path further
        for decryption, while that is done it returns a password to a give site specified by
        a user.

        - key_path:         path to where user key file is stored
        - path:             path to where users passwords file is stored
        - site:             website or name to any given thing to which password will be give to a user """

        with open(key_path, 'rb') as file:
            self.key = file.readline()

        self.load_password_file(path)

        return self.password_dict[site]
