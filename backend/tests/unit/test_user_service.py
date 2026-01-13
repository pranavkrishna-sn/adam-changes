import pytest
from backend.models.user import User
from backend.repositories.user_repository import UserRepository
from backend.services.user_service import UserService

class InMemoryRepository(UserRepository):
    def __init__(self) -> None:
        self.users = {}

    def create_user(self, user: User) -> User:
        if user.email in self.users:
            raise ValueError("Email already exists")
        user.id = len(self.users) + 1
        self.users[user.email] = user
        return user

    def get_by_email(self, email: str):
        return self.users.get(email)

@pytest.fixture
def user_service() -> UserService:
    repo = InMemoryRepository()
    return UserService(repository=repo)

def test_register_user_success(user_service: UserService):
    user = user_service.register_user("test@example.com", "securepassword")
    assert user.id == 1
    assert user.email == "test@example.com"

def test_register_user_duplicate_email(user_service: UserService):
    user_service.register_user("dup@example.com", "securepassword")
    with pytest.raises(ValueError):
        user_service.register_user("dup@example.com", "securepassword")