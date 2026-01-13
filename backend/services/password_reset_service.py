import secrets
import hashlib
import logging
from datetime import datetime, timedelta
from backend.models.password_reset import PasswordResetToken
from backend.repositories.password_reset_repository import PasswordResetRepository
from backend.repositories.user_repository import UserRepository
from backend.config.settings import Settings
import bcrypt

logger = logging.getLogger("ecommerce")

class PasswordResetService:
    def __init__(self, user_repo: UserRepository, reset_repo: PasswordResetRepository, settings: Settings) -> None:
        self.user_repo = user_repo
        self.reset_repo = reset_repo
        self.settings = settings

    def request_password_reset(self, email: str) -> str:
        user = self.user_repo.get_by_email(email)
        if not user:
            raise ValueError("No account associated with provided email")

        raw_token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
        expires_at = datetime.utcnow() + timedelta(hours=self.settings.password_reset_expiry_hours)
        reset_token = PasswordResetToken(user_id=user.id, token=token_hash, expires_at=expires_at)
        self.reset_repo.create_token(reset_token)

        logger.info("Password reset link generated for email %s", email)
        return raw_token  # Send this raw token via email in production

    def reset_password(self, token: str, new_password: str) -> None:
        token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
        reset_entry = self.reset_repo.get_token(token_hash)
        if not reset_entry:
            raise ValueError("Invalid or expired reset token")
        if reset_entry.used:
            raise ValueError("Reset token has already been used")
        if datetime.utcnow() > reset_entry.expires_at:
            raise ValueError("Reset token has expired")

        password_hash = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        self.user_repo.update_password(reset_entry.user_id, password_hash)
        self.reset_repo.mark_used(token_hash)
        logger.info("Password reset successful for token %s", token_hash)