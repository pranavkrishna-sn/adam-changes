import pytest
import bcrypt
from datetime import datetime, timedelta
from backend.models.user import User
from backend.models.password_reset import PasswordResetToken
from backend.repositories.user_repository import UserRepository
from backend.repositories.password_reset_repository import PasswordResetRepository
from backend.services.password_reset_service import PasswordResetService
from backend.config.settings import Settings

class InMemoryUserRepo(UserRepository):
    def __init__(self):
        self.users = {1: User(id=1, email="test@example.com", password_hash="hash")}

    def get_by_email(self, email: str):
        for user in self.users.values():
            if user.email == email:
                return user
        return None

    def update_password(self, user_id: int, new_hash: str):
        self.users[user_id].password_hash = new_hash

class InMemoryResetRepo(PasswordResetRepository):
    def __init__(self):
        self.tokens = {}

    def create_token(self, token: PasswordResetToken):
        token.id = len(self.tokens) + 1
        self.tokens[token.token] = token
        return token

    def get_token(self, token_str: str):
        return self.tokens.get(token_str)

    def mark_used(self, token_str: str):
        if token_str in self.tokens:
            self.tokens[token_str].used = True

@pytest.fixture
def service():
    user_repo = InMemoryUserRepo()
    reset_repo = InMemoryResetRepo()
    settings = Settings()
    return PasswordResetService(user_repo, reset_repo, settings)

def test_password_reset_request(service):
    token = service.request_password_reset("test@example.com")
    assert token is not None

def test_invalid_email_for_reset(service):
    with pytest.raises(ValueError):
        service.request_password_reset("non_existent@example.com")

def test_token_expiry(service):
    token = service.request_password_reset("test@example.com")
    reset_entry = list(service.reset_repo.tokens.values())[0]
    reset_entry.expires_at = datetime.utcnow() - timedelta(hours=1)
    with pytest.raises(ValueError):
        service.reset_password(token, "newpassword123")