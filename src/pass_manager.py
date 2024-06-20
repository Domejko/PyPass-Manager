from typing import Type
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
import hashlib
import sqlite3

from src.tools import (
    users_list,
    store_directory_paths,
    prefix_generator,
    get_user_dir,
    create_users_list,
)


class PasswordManager:
    def __init__(self) -> None:
        self.key = None
        self.password_file = None
        self.password_dict = {}

    def create_key(self, key_path: str, password: str, user_name: str) -> bool:
        """Generate binary key for a given account. Create sql database where key, login, password
        and used salt are stored and returns bool value to provide a feedback th the user.

        :param key_path: directory of where they file will be stored
        :param password: new user password
        :param user_name: new user login"""

        salt = Fernet.generate_key()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA3_512(), length=32, salt=salt, iterations=1480000
        )
        self.key = base64.urlsafe_b64encode(kdf.derive(password.encode()))

        hashed_pass = hashlib.pbkdf2_hmac(
            hash_name="sha3-512",
            password=password.encode(),
            salt=salt,
            iterations=1500000,
        )
        hashed_login = hashlib.pbkdf2_hmac(
            hash_name="sha3-512",
            password=user_name.encode(),
            salt=salt,
            iterations=1500000,
        )

        try:
            dbase = sqlite3.connect(key_path)
            curs = dbase.cursor()

            curs.execute(
                """
            CREATE TABLE IF NOT EXISTS userdata (
                data1 VARCHAR(255) NOT NULL,
                data2 VARCHAR(255) NOT NULL,
                data3 VARCHAR(255) NOT NULL,
                data4 VARCHAR(255) NOT NULL)
                """
            )
            curs.execute(
                "INSERT INTO userdata (data1, data2, data3, data4) VALUES (?, ?, ?, ?)",
                (self.key, hashed_login, hashed_pass, salt),
            )

            dbase.commit()
            dbase.close()

            return True
        except PermissionError:
            return False

    def create_password_file(
        self, path: str, key_path: str, initial_values: dict = None
    ) -> None:
        """Create a file where hashed users passwords will be stored passing further information
        that will be hashed and saved in created file.

         :param path: directory of where uses password will be stored
         :param key_path: direction of where user key will be stored
         :param initial_values: dictionary containing specific account login and password"""

        self.password_file = path

        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb"):
            pass

        if initial_values is not None:
            for user, password in initial_values.items():
                self.add_password(user, password, key_path, path)

    def create_new_user(
        self, user_name: str, password: str, key_file_path: str
    ) -> Type[PermissionError] | bool:
        """Checks for duplicate account names. \n
        Prepare new paths variables which are further passed to another functions/methods that create
        directories and files for new user. \n
        Prepare given new user information and passing them to another functions/methods for further
        processing.

        :param user_name: login of a give new user
        :param password: password to account of a give new user
        :param key_file_path: directory selected by a user where those files will be created
        """

        if users_list(user_name):
            return False

        head, tail = get_user_dir()
        hashed = hashlib.sha3_512(user_name.encode("utf-8")).hexdigest()

        new_key_path = key_file_path + f"/{prefix_generator(16)}.db"
        new_sites_path = head + tail + f"/{prefix_generator(16)}.bin"

        if os.path.isfile(new_key_path) or os.path.isfile(new_sites_path):
            new_key_path = key_file_path + f"/{prefix_generator(24)}.db"
            new_sites_path = head + tail + f"/{prefix_generator(24)}.bin"

        if self.create_key(new_key_path, password, user_name):
            if not os.path.exists(head + tail):
                os.makedirs(head + tail)
            elif not os.path.exists(key_file_path):
                os.makedirs(key_file_path)
            with open(new_sites_path, "wb"):
                pass

            store_directory_paths(user_name, new_key_path, new_sites_path, hashed)
            create_users_list(user_name)
            return True

        else:
            return PermissionError

    def load_password_file(self, path: str) -> None:
        """Loads a file from a given path where encrypted passwords are stored and with a give
        key decrypt them and save in a variable.

        :param path: path with a file containing passwords to account or sites"""

        self.password_file = path

        with open(path, "r") as file:
            for line in file:
                try:
                    site, encrypted = line.split(":")
                    site = Fernet(self.key).decrypt(site.encode()).decode()
                    self.password_dict[site] = (
                        Fernet(self.key).decrypt(encrypted.encode()).decode()
                    )
                except ValueError:
                    continue

    def add_password(
        self, site: str, password: str, key_path: str, site_path: str
    ) -> None:
        """With a specific key unique to every account this method opens a path where given user
        passwords are stored and with that specific key encrypts passwords and add them to a file.

        :param site: website or name to any given thing to which password will be assigned \n
        :param password: password to that given site/thing that will be stored with it \n
        :param key_path: path to where user key file is stored \n
        :param site_path: path to where users sites passwords file is stored"""

        dbase = sqlite3.connect(key_path)
        curs = dbase.cursor()

        curs.execute("SELECT data1 FROM userdata")
        raw_data = curs.fetchone()
        self.key = raw_data[0]

        dbase.close()

        self.load_password_file(site_path)
        self.password_dict[site] = password

        if self.password_file is not None:
            with open(self.password_file, "a+") as file:
                encrypted_login = Fernet(self.key).encrypt(site.encode())
                encrypted_password = Fernet(self.key).encrypt(password.encode())
                file.write(
                    encrypted_login.decode() + ":" + encrypted_password.decode() + "\n"
                )

    def get_pass(self, key_path: str, path: str, site: str = None) -> str | dict:
        """With a give key path it's storing key value to a variable and passing site_path further
        for decryption, while that is done it returns a password to a give site specified by
        a user.

        :param key_path: path to where user key file is stored
        :param path: path to where users passwords file is stored
        :param site: website or name to any given thing to which password will be give to a user
        """

        dbase = sqlite3.connect(key_path)
        curs = dbase.cursor()

        curs.execute("SELECT data1 FROM userdata")
        raw_data = curs.fetchone()
        self.key = raw_data[0]

        dbase.close()

        self.load_password_file(path)

        if site is None:
            return self.password_dict
        else:
            return self.password_dict[site]

    @staticmethod
    def get_encrypted(key_path: str) -> tuple[bytes, bytes]:
        """With a given path to sql database it gets user hashed credentials and returns them for
        login confirmation.

        :param key_path: path to where user key file is stored"""

        dbase = sqlite3.connect(key_path)
        curs = dbase.cursor()

        curs.execute("SELECT * FROM userdata")
        raw_data = curs.fetchall()
        login = raw_data[0][1]
        password = raw_data[0][2]

        dbase.close()

        return login, password

    @staticmethod
    def encrypt_password(
        key_path: str, password: str, user_name: str
    ) -> tuple[bytes, bytes]:
        """Encrypts login and password input and returns it for login comparison.

        :param key_path: path to where user key file is stored
        :param password: password taken from login window input
        :param user_name: user_name taken from login window input"""

        dbase = sqlite3.connect(key_path)
        curs = dbase.cursor()

        curs.execute("SELECT data4 FROM userdata")
        raw_data = curs.fetchone()
        salt = raw_data[0]

        dbase.close()

        hashed_pass = hashlib.pbkdf2_hmac(
            hash_name="sha3-512",
            password=password.encode(),
            salt=salt,
            iterations=1500000,
        )
        hashed_login = hashlib.pbkdf2_hmac(
            hash_name="sha3-512",
            password=user_name.encode(),
            salt=salt,
            iterations=1500000,
        )

        return hashed_login, hashed_pass
