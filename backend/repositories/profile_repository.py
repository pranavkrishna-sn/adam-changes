import sqlite3
import logging
from typing import Optional
from backend.models.user_profile import UserProfile

logger = logging.getLogger("ecommerce")

class ProfileRepository:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def get_profile(self, user_id: int) -> Optional[UserProfile]:
        query = """
        SELECT id, user_id, full_name, email, phone_number, address, preferences, created_at, updated_at
        FROM user_profiles WHERE user_id = ?
        """
        with self._get_connection() as conn:
            row = conn.execute(query, (user_id,)).fetchone()
            if not row:
                return None
            return UserProfile(
                id=row[0], user_id=row[1], full_name=row[2], email=row[3],
                phone_number=row[4], address=row[5], preferences=row[6],
                created_at=row[7], updated_at=row[8]
            )

    def update_profile(self, profile: UserProfile) -> UserProfile:
        query = """
        UPDATE user_profiles
        SET full_name = ?, email = ?, phone_number = ?, address = ?, preferences = ?, updated_at = CURRENT_TIMESTAMP
        WHERE user_id = ?
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (profile.full_name, profile.email, profile.phone_number,
                                   profile.address, profile.preferences, profile.user_id))
            if cursor.rowcount == 0:
                raise ValueError("Profile not found for user")
            conn.commit()
        logger.info("Profile updated for user_id=%s", profile.user_id)
        return self.get_profile(profile.user_id)

    def create_profile(self, profile: UserProfile) -> UserProfile:
        query = """
        INSERT INTO user_profiles (user_id, full_name, email, phone_number, address, preferences, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (
                profile.user_id, profile.full_name, profile.email,
                profile.phone_number, profile.address, profile.preferences,
                profile.created_at, profile.updated_at
            ))
            conn.commit()
            profile.id = cursor.lastrowid
        logger.info("New profile created for user_id=%s", profile.user_id)
        return profile