from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./database/ecommerce.db"
    admin_api_key: str = "replace_me_securely"

    class Config:
        env_file = ".env"