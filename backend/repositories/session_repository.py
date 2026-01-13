import sqlite3
import logging
from typing import Optional
from backend.models.session import Session

logger = logging.getLogger("ecommerce")

class SessionRepository:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def create_session(self, session: Session) -> Session:
        query = """
        INSERT INTO sessions (user_id, token, created_at, last_activity_at, is_active)
        VALUES (?, ?, ?, ?, ?)
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (session.user_id, session.token, session.created_at, session.last_activity_at, session.is_active))
            conn.commit()
            session.id = cursor.lastrowid
            logger.info("Session created for user_id %s", session.user_id)
            return session

    def get_active_session(self, user_id: int) -> Optional[Session]:
        query = "SELECT id, user_id, token, created_at, last_activity_at, is_active FROM sessions WHERE user_id = ? AND is_active = 1"
        with self._get_connection() as conn:
            row = conn.execute(query, (user_id,)).fetchone()
            if not row:
                return None
            return Session(id=row[0], user_id=row[1], token=row[2], created_at=row[3], last_activity_at=row[4], is_active=bool(row[5]))

    def deactivate_session(self, token: str) -> None:
        query = "UPDATE sessions SET is_active = 0 WHERE token = ?"
        with self._get_connection() as conn:
            conn.execute(query, (token,))
            conn.commit()