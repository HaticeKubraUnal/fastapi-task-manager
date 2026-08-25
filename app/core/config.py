#(Kasa ve Güvenlik Odası): Projenin beynidir. JWT Token üretildiği,
# şifrelerin kırılmaz hale (hash) getirildiği çok gizli güvenlik mekanizmaları bu odada yer alacak.

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()