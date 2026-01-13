import pytest
from backend.models.user_profile import UserProfile
from backend.repositories.profile_repository import ProfileRepository
from backend.services.profile_service import ProfileService

class InMemoryProfileRepository(ProfileRepository):
    def __init__(self):
        self.profiles = {}

    def get_profile(self, user_id: int):
        return self.profiles.get(user_id)

    def create_profile(self, profile: UserProfile):
        self.profiles[profile.user_id] = profile
        return profile

    def update_profile(self, profile: UserProfile):
        self.profiles[profile.user_id] = profile
        return profile

@pytest.fixture
def profile_service() -> ProfileService:
    repo = InMemoryProfileRepository()
    return ProfileService(repository=repo)

def test_create_user_profile(profile_service: ProfileService):
    data = {"full_name": "John Doe", "email": "john@example.com"}
    profile = profile_service.create_user_profile(1, data)
    assert profile.user_id == 1
    assert profile.full_name == "John Doe"

def test_update_user_profile(profile_service: ProfileService):
    data = {"full_name": "John Doe", "email": "john@example.com"}
    profile_service.create_user_profile(1, data)
    updated = profile_service.update_user_profile(1, {"full_name": "John Smith"})
    assert updated.full_name == "John Smith"

def test_get_missing_profile(profile_service: ProfileService):
    with pytest.raises(ValueError):
        profile_service.get_user_profile(99)