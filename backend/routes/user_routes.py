from fastapi import APIRouter, HTTPException, Depends, status
from backend.services.user_service import UserService
from backend.repositories.user_repository import UserRepository
from backend.config.settings import Settings

router = APIRouter()
settings = Settings()
repository = UserRepository(db_path="database/ecommerce.db")
service = UserService(repository=repository)

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(email: str, password: str) -> dict:
    try:
        user = service.register_user(email=email, password=password)
        return {"id": user.id, "email": user.email}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))