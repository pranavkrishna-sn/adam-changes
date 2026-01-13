from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./database/ecommerce.db"
    secret_key: str = "replace_me_in_prod"
    password_reset_expiry_hours: int = 24

    class Config:
        env_file = ".env"