from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import select
from models.User import User
from settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, TZ
import jwt
import bcrypt
from pytz import timezone
from datetime import datetime, timedelta

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token/")


def generate_hash_password(password: str) -> str:
    hash = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
    return hash.decode()


def validated_user_password(hash: str, password: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode(), hash.encode())
    except Exception:
        return False


async def generate_jwt_token_from_user(
    user: User, ignore_timezone: bool = False
) -> str:
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    if ignore_timezone is False:
        expire = expire.astimezone(timezone(TZ))
    """
    {
    "user_id": 671,
    "username": "addthoriq",
    "exp": 1641455971,
    "email": "thoriq@qti.co.id"
    }
    """
    payload = {
        "id": str(user.id),
        "email": user.email,
        "exp": expire,
    }
    jwt_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_token


def get_user_from_jwt_token(db: Session, jwt_token: str) -> Optional[User]:
    try:
        payload = jwt.decode(jwt_token, key=SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("id")
        query = select(User).filter(User.id == id)
        user = db.execute(query).scalar()
    except jwt.ExpiredSignatureError:
        return None
    return user
