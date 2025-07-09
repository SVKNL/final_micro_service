# from jwt.exceptions import InvalidTokenError
# from fastapi import APIRouter, HTTPException
# from fastapi.params import Depends, Form
# from fastapi.security import (HTTPBearer,
#                               HTTPAuthorizationCredentials,
#                               OAuth2PasswordBearer)
# from pydantic import BaseModel
# from starlette import status
#
# from src.schemas.user import UserDB
# from src.auth import utils as auth_utils
#
# router = APIRouter(prefix="/demo_jwt_auth", tags=["JWT"])
#
# http_bearer = HTTPBearer()
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/demo_jwt_auth/login/")
#
# class TokenInfo(BaseModel):
#     access_token: str
#     token_type: str
#
# john = UserSchema(
#     username = 'John',
#     password = auth_utils.hash_password('qwerty'),
#     email = 'john@google.com',
# )
#
# users_db: dict[str, UserDB] = {
#     john.username: john,
# }
#
# def validate_auth_user(
#         username: str = Form(),
#         password: str = Form(),
# ):
#     unauth_exc = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Incorrect username or password",
#     )
#     if not (user := users_db.get(username)):
#         raise unauth_exc
#     if auth_utils.validate_password(
#             password,
#             user.password
#     ):
#         return user
#     raise unauth_exc
#
#
# def get_current_token_payload(
#         #credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
#         token: str = Depends(oauth2_scheme),
# ) -> UserDB:
#     #token = credentials.credentials
#     try:
#         payload = auth_utils.decode_jwt(
#             token=token,
#         )
#     except InvalidTokenError as e:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail=str(e)
#         )
#     return payload
#
#
# def get_current_auth_user(
#         payload: dict = Depends(get_current_token_payload),
# ) -> UserDB:
#     username: str = payload.get('sub')
#     if username not in users_db:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Token not found(username not found)",
#         )
#     else:
#         return users_db.get(username)
#
#
# @router.post("/login/", response_model=TokenInfo)
# def auth_user_issue_jwt(
#         user: UserDB = Depends(validate_auth_user),
# ):
#     jwt_payload = {
#         'sub': user.username,
#         'email': user.email,
#         'username': user.username,
#     }
#     token = auth_utils.encode_jwt(jwt_payload)
#     return TokenInfo(
#         access_token=token,
#         token_type="Bearer"
#     )
#
# @router.get('/users/me')
# def auth_user_check_self_info(
#         user: UserDB = Depends(get_current_auth_user),
#         payload: dict = Depends(get_current_token_payload),
# ):
#     iat = payload.get('iat')
#     return {
#         'username': user.username,
#         'email': user.email,
#         'logged_in_at': iat
#     }