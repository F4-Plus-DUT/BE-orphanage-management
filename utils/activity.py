import secrets
import string


def read_content(filename: str):
    with open(filename, "r", encoding='utf-8') as f:
        text = f.read()
    return text


def gen_password():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(8))
    return password
