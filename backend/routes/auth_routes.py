from fastapi import APIRouter, HTTPException, status
from backend.repositories.user_repository import UserRepository
from backend.repositories.session_repository import SessionRepository
from backend.config.settings import Settings
from backend.services.auth_service import AuthService

router = APIRouter()
settings = Settings()
user_repo = UserRepository(db_path="database/ecommerce.db")
session_repo = SessionRepository(db_path="database/ecommerce.db")
auth_service = AuthService(user_repo, session_repo, settings)

@router.post("/login", status_code=status.HTTP_200_OK)
async def login(email: str, password: str) -> dict:
    try:
        token = auth_service.login(email=email, password=password)
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(token: str) -> dict:
    auth_service.logout(token)
    return {"message": "Session terminated successfully"}