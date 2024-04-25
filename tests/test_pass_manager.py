import os
import unittest
from unittest.mock import patch

from cryptography.fernet import Fernet

from src.pass_manager import PasswordManager


class TestPasswordManager(unittest.TestCase):
    def setUp(self):
        self.password_manager = PasswordManager()

        self.key_path = 'test_key.db'
        self.site_path = 'test_site.txt'
        self.pass_path = 'test_pass.txt'

        self.test_password = 'password'
        self.test_site = 'example.com'

    def tearDown(self):
        file_list = ['test_key.db', 'test_site.txt', 'test_pass.txt']
        for file in file_list:
            try:
                os.remove(file)
            except OSError:
                pass

    def test_create_key(self):
        user_name = "test_user"
        result = self.password_manager.create_key(self.key_path, self.test_password, user_name)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.key_path))

    def test_load_password_file(self):
        self.password_manager.create_key(self.key_path, self.test_password, 'user')
        site_encrypted = Fernet(self.password_manager.key).encrypt(self.test_site.encode())
        pass_encrypted = Fernet(self.password_manager.key).encrypt(self.test_password.encode())

        with open(self.pass_path, 'a+') as file:
            file.write(site_encrypted.decode() + ':' + pass_encrypted.decode() + '\n')

        self.password_manager.load_password_file(self.pass_path)
        self.assertEqual(self.password_manager.password_dict[self.test_site], self.test_password)

    def test_add_password(self):
        with open(self.site_path, 'wb') as f:
            pass

        self.password_manager.create_key(self.key_path, "password", "user")
        self.password_manager.add_password(self.test_site, self.test_password, self.key_path, self.site_path)

        with open(self.site_path, "r") as f:
            for line in f:
                site, password = line.split(':')
                site = Fernet(self.password_manager.key).decrypt(site.encode()).decode()
                password = Fernet(self.password_manager.key).decrypt(password.encode()).decode()
        self.assertEqual(self.test_site, site)
        self.assertEqual(self.test_password, password)

    @patch('src.pass_manager.PasswordManager.load_password_file', return_value=True)
    def test_get_pass(self, mock_load_password_file):
        self.password_manager.create_key(self.key_path, self.test_password, 'user')
        self.password_manager.password_dict = {self.test_site: self.test_password}

        with patch('sqlite3.connect') as mock_connect:
            self.password_manager.get_pass(self.key_path, self.pass_path, self.test_site)
            mock_connect.assert_called_once_with(self.key_path)

    def test_get_encrypted(self):
        self.password_manager.create_key(self.key_path, self.test_password, 'user')

        encrypted_login, encrypted_password = PasswordManager.get_encrypted(self.key_path)
        self.assertTrue(encrypted_login)
        self.assertTrue(encrypted_password)

    def test_encrypt_password(self):
        self.password_manager.create_key(self.key_path, self.test_password, 'user')

        with patch('hashlib.pbkdf2_hmac') as mock_hash:
            mock_hash.return_value = 'test_data'

            hashed_login, hashed_password = PasswordManager.encrypt_password(self.key_path, 'test', 'test')
            self.assertEqual(hashed_login, 'test_data')
            self.assertEqual(hashed_password, 'test_data')
