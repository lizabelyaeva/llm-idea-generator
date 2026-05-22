from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.entities import User


pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
bearer_scheme = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def create_access_token(*, user_id: int) -> str:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=settings.jwt_access_token_minutes)
    payload = {"sub": str(user_id), "iat": int(now.timestamp()), "exp": int(exp.timestamp())}
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")


def create_admin_token() -> str:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(hours=8)
    payload = {"scope": "admin", "iat": int(now.timestamp()), "exp": int(exp.timestamp())}
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")


def verify_admin_token(token: str) -> bool:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
    except JWTError:
        return False
    return payload.get("scope") == "admin"


def _decode_token(token: str) -> int:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
    except JWTError as exc:
        raise HTTPException(status_code=401, detail="Недействительный токен") from exc
    sub = payload.get("sub")
    if not sub:
        raise HTTPException(status_code=401, detail="Недействительный токен")
    try:
        return int(sub)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail="Недействительный токен") from exc


def get_current_user(
    creds: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    if creds is None or not creds.credentials:
        raise HTTPException(status_code=401, detail="Требуется авторизация")
    user_id = _decode_token(creds.credentials)
    user = db.query(User).filter(User.id == user_id).one_or_none()
    if user is None:
        raise HTTPException(status_code=401, detail="Пользователь не найден")
    return user
