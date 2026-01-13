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

    def create_user(self, user: User) -> User:
        query = """
        INSERT INTO users (email, password_hash, created_at, updated_at, is_active)
        VALUES (?, ?, ?, ?, ?)
        """
        with self._get_connection() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute(query, (user.email, user.password_hash, user.created_at, user.updated_at, user.is_active))
                conn.commit()
                user.id = cursor.lastrowid
                logger.info("User created with ID %s", user.id)
                return user
            except sqlite3.IntegrityError as e:
                logger.error("User creation failed: %s", e)
                raise ValueError("Email already exists") from e

    def get_by_email(self, email: str) -> Optional[User]:
        query = "SELECT id, email, password_hash, created_at, updated_at, is_active FROM users WHERE email = ?"
        with self._get_connection() as conn:
            row = conn.execute(query, (email,)).fetchone()
            if not row:
                return None
            return User(id=row[0], email=row[1], password_hash=row[2],
                        created_at=row[3], updated_at=row[4], is_active=bool(row[5]))