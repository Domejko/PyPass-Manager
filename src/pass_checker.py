import requests
import hashlib
from requests import Response


def request_api_data(query_char: str) -> Response:
    """Requesting a response from a fixed api url with a given query and checking for a response
    status, if it's correct we return response.

    :param query_char: hashed front half piece of a password we want to check"""

    header = {"Add-Padding": "true"}
    url = "https://api.pwnedpasswords.com/range/" + query_char
    response = requests.get(url, headers=header)
    response.raise_for_status()
    return response


def get_passwords_leak_count(hashes: hash, hash_to_check: str) -> int:
    """At first, it splits hashed response. Next it loop through a given response for password front
    and looks for a match with a tail of a password. If it finds a match it returns number of times pwned
    , when there is no match found it returns 0.

    :param hashes: hashed response on front password query from API \n
    :param hash_to_check: tail of a hashed password"""

    hashes = (line.split(":") for line in hashes.text.splitlines())
    for h, count in hashes:
        if hash_to_check in h:
            return count
    return 0


def pwned_api_check(password: str) -> int:
    """Take password as argument and hash it with SHA1, next it's split that password on front and tail
    feeding front part to a request function from which response with a password tail will be feed
    to a function that return number of times password was pwned and returns it.

    :param password: password which we want to check in a pwnedpasswords database.
    """

    # API require SHA1 hashing function
    hash_password = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    password_front, password_tail = hash_password[0:5], hash_password[5:]
    response = request_api_data(password_front)
    return get_passwords_leak_count(response, password_tail)


def run_program(password: str) -> int:
    """Main function that runs whole program and returns a number of times pwned given password was.

    :param password: password which we want to check"""

    count = pwned_api_check(password)
    return count
