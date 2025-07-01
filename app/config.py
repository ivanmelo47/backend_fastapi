# app/config.py

from pydantic_settings import BaseSettings
from zoneinfo import ZoneInfo

class Settings(BaseSettings):
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str
    MYSQL_PORT: str
    MYSQL_DB: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    TIMEZONE: str = "America/Mexico_City"  # ✅ Agregado aquí

    class Config:
        env_file = ".env"
        
    @property
    def tz(self) -> ZoneInfo:
        return ZoneInfo(self.TIMEZONE)

    @property
    def DATABASE_URL(self):
        return (
            f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@"
            f"{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}"
        )

settings = Settings()
