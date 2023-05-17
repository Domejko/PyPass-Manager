from Crypto.Cipher import AES


class DirectoryCipher:
    def __init__(self, key: bytes) -> None:
        """
        - key :              b string object of length 16/24/32 bytes
        """
        self.key = key

    @staticmethod
    def pad(data: bytes) -> bytes:
        """ Padding data to fit length expected by AES CBC mode.

        - data :             b string data string that is to be padded """

        return data + b"\0" * (AES.block_size - len(data) % AES.block_size)

    def encrypt_directory(self, data: bytes, iv: bytes) -> bytes:
        """ At first, it creates cipher object with a given key after that with that object
        padded data is encoded and returned along with initialization vector created from
        hashed username.


        - data :             data for encryption as b string
        - iv :               b string initialization vector 16 bytes of length """

        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        padded_data = self.pad(data)
        encrypted_data = cipher.encrypt(padded_data)
        return iv + encrypted_data

    def decrypt_directory(self, data: bytes) -> bytes:
        """ Splits received data on initialization vector and encrypted data. With a given key
        creates cipher object that will be used to decrypt data which will be returned in
        format of a b string.

        - data :             encrypted data """

        iv = data[:16]
        data = data[16:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted_data = cipher.decrypt(data)
        return decrypted_data.rstrip(b"\0")
