from datetime import datetime, timedelta, UTC

from jose import jwt

from app.core.config import settings


def create_access_token(data: dict):

    payload = data.copy()

    expire = datetime.now(UTC) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload.update({"exp": expire})

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm,
    )


def decode_access_token(token: str):

    return jwt.decode(
        token,
        settings.secret_key,
        algorithms=[settings.algorithm],
    )