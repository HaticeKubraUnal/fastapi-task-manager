# Kodun içine açıkça yazılmaması gereken .env dosyasındaki şifreleri güvenli bir şekilde çekip Python'un kullanabileceği hale getirir.

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()