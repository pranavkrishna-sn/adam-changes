import sqlite3
import logging
from typing import Optional
from datetime import datetime
from backend.models.password_reset import PasswordResetToken

logger = logging.getLogger("ecommerce")

class PasswordResetRepository:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def create_token(self, token: PasswordResetToken) -> PasswordResetToken:
        query = """
        INSERT INTO password_reset_tokens (user_id, token, expires_at, created_at, used)
        VALUES (?, ?, ?, ?, ?)
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (token.user_id, token.token, token.expires_at, token.created_at, token.used))
            conn.commit()
            token.id = cursor.lastrowid
        logger.info("Password reset token created for user_id=%s", token.user_id)
        return token

    def get_token(self, token_str: str) -> Optional[PasswordResetToken]:
        query = "SELECT id, user_id, token, expires_at, created_at, used FROM password_reset_tokens WHERE token = ?"
        with self._get_connection() as conn:
            row = conn.execute(query, (token_str,)).fetchone()
            if not row:
                return None
            return PasswordResetToken(id=row[0], user_id=row[1], token=row[2], expires_at=row[3], created_at=row[4], used=bool(row[5]))

    def mark_used(self, token_str: str) -> None:
        query = "UPDATE password_reset_tokens SET used = 1 WHERE token = ?"
        with self._get_connection() as conn:
            conn.execute(query, (token_str,))
            conn.commit()
        logger.info("Password reset token marked as used: %s", token_str)