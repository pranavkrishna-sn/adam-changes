from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./database/ecommerce.db"

    class Config:
        env_file = ".env"