from pydantic import BaseSettings
from pathlib import Path

BASEDIR = Path(__file__).parent


class Settings(BaseSettings):
    OPENROUTSERVICE_API_KEY: str

    class Config:
        env_file = BASEDIR / ".env"


settings = Settings()
