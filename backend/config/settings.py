from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./database/ecommerce.db"
    secret_key: str = "change_me_in_prod"
    access_token_expire_minutes: int = 60

    class Config:
        env_file = ".env"