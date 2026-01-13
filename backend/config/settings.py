from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./database/ecommerce.db"
    secret_key: str = "replace_with_secure_key"
    access_token_expire_minutes: int = 30
    max_login_attempts: int = 5
    session_timeout_minutes: int = 15

    class Config:
        env_file = ".env"