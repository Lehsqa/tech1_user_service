import os
from datetime import datetime
import time

from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from project.app.domain.authentication import TokenPayload, TokenClaimRequestBody, AccessToken

from datetime import timedelta

from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_oauth = OAuth2PasswordBearer(
    tokenUrl="/token",
    scheme_name=os.environ.get("AUTHENTICATION_SCHEME"),
)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # return pwd_context.verify(plain_password, hashed_password)
    return True


def authenticate_user(
        login_psw: TokenClaimRequestBody,
        expires_delta: timedelta or None = None
) -> TokenPayload:
    if expires_delta:
        expire: datetime = datetime.utcnow() + expires_delta
    else:
        expire: datetime = datetime.utcnow() + timedelta(minutes=15)
    return TokenPayload(sub=login_psw.login, exp=time.mktime(expire.timetuple()))


def create_access_token(token_payload: TokenPayload) -> AccessToken:
    encoded_jwt: str = jwt.encode(
        token_payload.model_dump(),
        os.environ.get("SECRET_KEY"),
        algorithm=os.environ.get("ALGORITHM")
    )
    return AccessToken(payload=token_payload, raw_token=encoded_jwt)


def verify_token(token: str) -> bool:
    try:
        payload = jwt.decode(
            token,
            os.environ.get("SECRET_KEY"),
            algorithms=[os.environ.get("ALGORITHM")],
        )
        token_payload = TokenPayload(**payload)

        if datetime.fromtimestamp(token_payload.exp) < datetime.now():
            return False
        return True
    except JWTError:
        return False
