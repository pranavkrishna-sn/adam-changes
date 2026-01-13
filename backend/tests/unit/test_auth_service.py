import pytest
import bcrypt
from backend.models.user import User
from backend.repositories.user_repository import UserRepository
from backend.repositories.session_repository import SessionRepository
from backend.services.auth_service import AuthService
from backend.config.settings import Settings

class InMemoryUserRepo(UserRepository):
    def __init__(self):
        self.users = {}

    def get_by_email(self, email: str):
        return self.users.get(email)

    def update_login_attempts(self, email: str, attempts: int, locked: bool):
        user = self.users[email]
        user.login_attempts = attempts
        user.is_locked = locked

    def reset_login_attempts(self, email: str):
        user = self.users[email]
        user.login_attempts = 0
        user.is_locked = False

class InMemorySessionRepo(SessionRepository):
    def __init__(self):
        self.sessions = {}

    def create_session(self, session):
        self.sessions[session.token] = session
        return session

    def deactivate_session(self, token: str):
        self.sessions[token].is_active = False

@pytest.fixture
def auth_service():
    settings = Settings()
    user_repo = InMemoryUserRepo()
    session_repo = InMemorySessionRepo()
    password_hash = bcrypt.hashpw("password123".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    user_repo.users["test@example.com"] = User(id=1, email="test@example.com", password_hash=password_hash)
    return AuthService(user_repo, session_repo, settings)

def test_successful_login(auth_service):
    token = auth_service.login("test@example.com", "password123")
    assert token is not None

def test_failed_login_attempt_increments(auth_service):
    with pytest.raises(ValueError):
        auth_service.login("test@example.com", "badpass")
    user = auth_service.user_repo.users["test@example.com"]
    assert user.login_attempts == 1

def test_user_lockout_after_max_attempts(auth_service):
    for _ in range(auth_service.settings.max_login_attempts):
        try:
            auth_service.login("test@example.com", "wrongpassword")
        except ValueError:
            pass
    user = auth_service.user_repo.users["test@example.com"]
    assert user.is_locked