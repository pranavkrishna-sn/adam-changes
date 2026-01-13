import bcrypt
import jwt
import logging
from datetime import datetime, timedelta
from backend.models.session import Session
from backend.repositories.user_repository import UserRepository
from backend.repositories.session_repository import SessionRepository
from backend.config.settings import Settings

logger = logging.getLogger("ecommerce")

class AuthService:
    def __init__(self, user_repo: UserRepository, session_repo: SessionRepository, settings: Settings):
        self.user_repo = user_repo
        self.session_repo = session_repo
        self.settings = settings

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

    def _generate_token(self, user_id: int) -> str:
        payload = {
            "sub": str(user_id),
            "exp": datetime.utcnow() + timedelta(minutes=self.settings.access_token_expire_minutes)
        }
        return jwt.encode(payload, self.settings.secret_key, algorithm="HS256")

    def login(self, email: str, password: str) -> str:
        user = self.user_repo.get_by_email(email)
        if not user:
            raise ValueError("Invalid credentials")
        if user.is_locked:
            raise ValueError("Account locked due to multiple invalid attempts")

        if not self._verify_password(password, user.password_hash):
            attempts = user.login_attempts + 1
            locked = attempts >= self.settings.max_login_attempts
            self.user_repo.update_login_attempts(email, attempts, locked)
            logger.warning("Failed login attempt for %s (%s/%s)", email, attempts, self.settings.max_login_attempts)
            raise ValueError("Invalid credentials")
        
        self.user_repo.reset_login_attempts(email)
        token = self._generate_token(user.id)
        new_session = Session(user_id=user.id, token=token)
        self.session_repo.create_session(new_session)
        logger.info("User %s logged in successfully", email)
        return token

    def logout(self, token: str) -> None:
        self.session_repo.deactivate_session(token)
        logger.info("Session invalidated")