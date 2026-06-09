import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

SECRET_KEY: str = os.getenv("SECRET_KEY", "changeme-super-secret-key-for-dev-only")
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS: int = 300
REFRESH_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7  # 7 days

# Simulated user database — store pre-hashed passwords
USERS: dict[str, bytes] = {
    "admin": bcrypt.hashpw(b"admin123", bcrypt.gensalt()),
}


def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password)


def authenticate_user(username: str, password: str) -> bool:
    hashed = USERS.get(username)
    if not hashed:
        return False
    return verify_password(password, hashed)


def create_access_token(subject: str) -> str:
    now = datetime.now(tz=timezone.utc)
    payload = {
        "sub": subject,
        "iat": now,
        "exp": now + timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS),
        "type": "access",
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(subject: str) -> str:
    now = datetime.now(tz=timezone.utc)
    payload = {
        "sub": subject,
        "iat": now,
        "exp": now + timedelta(seconds=REFRESH_TOKEN_EXPIRE_SECONDS),
        "type": "refresh",
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    """Decode and validate a JWT. Raises jwt.PyJWTError on failure."""
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
