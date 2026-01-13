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
        query = "SELECT id, email, password_hash, login_attempts, is_locked, created_at, updated_at, is_active FROM users WHERE email = ?"
        with self._get_connection() as conn:
            row = conn.execute(query, (email,)).fetchone()
            if not row:
                return None
            return User(
                id=row[0], email=row[1], password_hash=row[2],
                login_attempts=row[3], is_locked=bool(row[4]),
                created_at=row[5], updated_at=row[6], is_active=bool(row[7])
            )

    def update_login_attempts(self, email: str, attempts: int, locked: bool) -> None:
        query = "UPDATE users SET login_attempts = ?, is_locked = ?, updated_at = CURRENT_TIMESTAMP WHERE email = ?"
        with self._get_connection() as conn:
            conn.execute(query, (attempts, int(locked), email))
            conn.commit()

    def reset_login_attempts(self, email: str) -> None:
        query = "UPDATE users SET login_attempts = 0, is_locked = 0, updated_at = CURRENT_TIMESTAMP WHERE email = ?"
        with self._get_connection() as conn:
            conn.execute(query, (email,))
            conn.commit()