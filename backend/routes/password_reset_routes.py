from fastapi import APIRouter, HTTPException, status
from backend.config.settings import Settings
from backend.repositories.user_repository import UserRepository
from backend.repositories.password_reset_repository import PasswordResetRepository
from backend.services.password_reset_service import PasswordResetService

router = APIRouter()
settings = Settings()
user_repo = UserRepository(db_path="database/ecommerce.db")
reset_repo = PasswordResetRepository(db_path="database/ecommerce.db")
service = PasswordResetService(user_repo, reset_repo, settings)

@router.post("/request", status_code=status.HTTP_200_OK)
async def request_reset(email: str) -> dict:
    try:
        token = service.request_password_reset(email)
        return {"message": "Password reset link generated successfully", "token_preview": token[:10] + "..."}  # In production, send via email
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/confirm", status_code=status.HTTP_200_OK)
async def reset_password(token: str, new_password: str) -> dict:
    try:
        service.reset_password(token, new_password)
        return {"message": "Password updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))