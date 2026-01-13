import logging
from backend.models.user_profile import UserProfile
from backend.repositories.profile_repository import ProfileRepository

logger = logging.getLogger("ecommerce")

class ProfileService:
    def __init__(self, repository: ProfileRepository) -> None:
        self.repository = repository

    def get_user_profile(self, user_id: int) -> UserProfile:
        profile = self.repository.get_profile(user_id)
        if not profile:
            raise ValueError("Profile not found")
        return profile

    def update_user_profile(self, user_id: int, data: dict) -> UserProfile:
        profile = self.repository.get_profile(user_id)
        if not profile:
            raise ValueError("Profile not found")
        for key, value in data.items():
            if hasattr(profile, key):
                setattr(profile, key, value)
        updated = self.repository.update_profile(profile)
        logger.info("Profile updated successfully for user_id=%s", user_id)
        return updated

    def create_user_profile(self, user_id: int, data: dict) -> UserProfile:
        new_profile = UserProfile(user_id=user_id, **data)
        created = self.repository.create_profile(new_profile)
        logger.info("Profile created successfully for user_id=%s", user_id)
        return created