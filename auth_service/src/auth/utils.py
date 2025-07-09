from jwt.exceptions import InvalidTokenError
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Form
from fastapi.security import (HTTPBearer,
                              HTTPAuthorizationCredentials,
                              OAuth2PasswordBearer)
from datetime import timedelta, datetime

import bcrypt
import jwt
from fastapi import HTTPException
from fastapi.params import Depends, Form
from pydantic import BaseModel
from starlette import status

from src.api.v1.services.user import UsersService
from src.config import settings
from src.schemas.user import UserDB


def encode_jwt(
        payload: dict,
        private_key: str = settings.auth_jwt.private_key_path.read_text(),
        algorithm: str =settings.auth_jwt.algorithm,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
        expire_timedelta: timedelta = None
):
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp = expire,
        iat = now,
    )
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm
    )
    return encoded


def decode_jwt(
        token: str | bytes,
        public_key: str = settings.auth_jwt.public_key_path.read_text(),
        algorithm: str =settings.auth_jwt.algorithm
):
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded

def hash_password(
        password: str,
) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)

def validate_password(
        password: str,
        hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password.encode(),
        hashed_password
    )


async def validate_auth_user(
        username: str = Form(),
        password: str = Form(),
        service: UsersService = Depends(),
):
    unauth_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
    )
    print(username, password)
    user = await service.get_by_username(username)
    print(user)
    if not user:
        raise unauth_exc
    user.password = user.password.encode('utf-8')
    print(user)
    if validate_password(
            password,
            user.password
    ):
        return user
    raise unauth_exc

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login/")

class TokenInfo(BaseModel):
    access_token: str
    token_type: str


def get_current_token_payload(
        token: str = Depends(oauth2_scheme),
) -> UserDB:

    try:
        payload = decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    return payload


async def get_current_auth_user(
        payload: dict = Depends(get_current_token_payload),
        service: UsersService = Depends(),
) -> UserDB:
    username: str = payload.get('sub')
    user = await service.get_by_username(username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not found(username not found)",
        )
    else:
        return user.username
