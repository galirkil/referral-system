import secrets
import string


def generate_authentication_code(length=4):
    code = "".join(secrets.choice(string.digits) for _ in range(length))
    return code
