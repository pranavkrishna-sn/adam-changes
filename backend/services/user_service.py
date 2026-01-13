import bcrypt
import logging
from backend.models.user import User
from backend.repositories.user_repository import UserRepository

logger = logging.getLogger("ecommerce")

class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def _hash_password(self, password: str) -> str:
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    def register_user(self, email: str, password: str) -> User:
        if self.repository.get_by_email(email):
            raise ValueError("Email already exists")
        password_hash = self._hash_password(password)
        new_user = User(email=email, password_hash=password_hash)
        created_user = self.repository.create_user(new_user)
        logger.info("Registered new user: %s", created_user.email)
        return created_user