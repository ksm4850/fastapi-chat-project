import bcrypt

from .repository import UserRepository


def hash_password(password: str) -> str:
    byte_password = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(byte_password, salt)
    return hashed_password.decode("utf-8")


def check_password(hashed_password: str, user_password: str) -> bool:
    byte_password = user_password.encode("utf-8")
    return bcrypt.checkpw(byte_password, hashed_password.encode("utf-8"))


class UserService:
    # repository: UserRepository

    def __init__(self, repository: UserRepository):
        self.repository = repository
