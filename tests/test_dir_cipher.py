import unittest
from Crypto.Cipher import AES

from src.dir_cipher import DirectoryCipher


class TestDirectoryCipher(unittest.TestCase):

    def setUp(self):
        self.key = b"0123456789abcdef"
        self.encrypted = (
            b"1234567890abcdef\x17\xd7\xc4\xde5\x00\x8abe\xa4\xc6\xba\x05`\x9c\x14"
        )
        self.directory_cipher = DirectoryCipher(self.key)

    def test_pad(self):
        data = b"test"
        padded_data = self.directory_cipher.pad(data)
        self.assertEqual(len(padded_data) % AES.block_size, 0)

    def test_encrypt_decrypt_directory(self):
        data = b"Hello, World!"
        iv = b"1234567890abcdef"
        encrypted_data = self.directory_cipher.encrypt_directory(data, iv)
        decrypted_data = self.directory_cipher.decrypt_directory(encrypted_data)

        self.assertEqual(encrypted_data, self.encrypted)
        self.assertEqual(decrypted_data, data)
