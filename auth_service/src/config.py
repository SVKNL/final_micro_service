import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from pydantic import BaseModel

load_dotenv(find_dotenv('.env'))

BASE_DIR = Path(__file__).parent.parent

class AuthJWT(BaseModel):
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15


class Settings:
    MODE: str = os.environ.get('MODE')

    DB_HOST: str = os.environ.get('DB_HOST')
    DB_PORT: int = os.environ.get('DB_PORT')
    DB_USER: str = os.environ.get('DB_USER')
    DB_PASS: str = os.environ.get('DB_PASS')
    DB_NAME: str = os.environ.get('DB_NAME')

    DB_URL: str = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

    auth_jwt: AuthJWT = AuthJWT()

settings = Settings()



