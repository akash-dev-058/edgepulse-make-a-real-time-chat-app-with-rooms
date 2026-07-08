import secrets
from datetime import datetime, timedelta
from typing import Optional, Union

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT utilities

def create_access_token(subject: Union[str, int], expires_delta: Optional[timedelta] = None) -> str:
    now = datetime.utcnow()
    expire = now + (expires_delta or timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = {"exp": expire, "iat": now, "sub": str(subject), "type": "access"}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, int], expires_delta: Optional[timedelta] = None) -> str:
    now = datetime.utcnow()
    expire = now + (expires_delta or timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS))
    to_encode = {"exp": expire, "iat": now, "sub": str(subject), "type": "refresh"}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def verify_token(token: str, token_type: str = "access") -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        if payload.get("type") != token_type:
            return None
        return payload
    except Exception:
        return None


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def generate_room_slug(name: str) -> str:
    # Sanitize and generate URL-friendly slug
    slug = name.lower().strip().replace(" ", "-")
    return slug + "-" + secrets.token_hex(4)
