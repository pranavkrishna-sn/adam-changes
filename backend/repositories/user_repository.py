import sqlite3
import logging
from typing import Optional
from backend.models.user import User

logger = logging.getLogger("ecommerce")

class UserRepository:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def get_by_email(self, email: str) -> Optional[User]:
        query = "SELECT id, email, password_hash, created_at, updated_at, is_active FROM users WHERE email = ?"
        with self._get_connection() as conn:
            row = conn.execute(query, (email,)).fetchone()
            if not row:
                return None
            return User(id=row[0], email=row[1], password_hash=row[2], created_at=row[3], updated_at=row[4], is_active=bool(row[5]))

    def update_password(self, user_id: int, new_hash: str) -> None:
        query = "UPDATE users SET password_hash = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
        with self._get_connection() as conn:
            conn.execute(query, (new_hash, user_id))
            conn.commit()
        logger.info("Password updated for user_id=%s", user_id)