from fastapi import APIRouter, HTTPException, status
from backend.repositories.profile_repository import ProfileRepository
from backend.services.profile_service import ProfileService
from backend.config.settings import Settings

router = APIRouter()
settings = Settings()
repo = ProfileRepository(db_path="database/ecommerce.db")
service = ProfileService(repository=repo)

@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_profile(user_id: int) -> dict:
    try:
        profile = service.get_user_profile(user_id)
        return {"profile": profile.dict()}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put("/{user_id}", status_code=status.HTTP_200_OK)
async def update_profile(user_id: int, data: dict) -> dict:
    try:
        updated = service.update_user_profile(user_id, data)
        return {"message": "Profile updated successfully", "profile": updated.dict()}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/{user_id}", status_code=status.HTTP_201_CREATED)
async def create_profile(user_id: int, data: dict) -> dict:
    try:
        profile = service.create_user_profile(user_id, data)
        return {"message": "Profile created successfully", "profile": profile.dict()}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))