from fastapi import HTTPException
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt
from sqlalchemy.orm import Session as SqlAlchemySession
from models import Session
from models.User import User
from settings import (
JWT_PREFIX,
SECRET_KEY,
ALGORITHM,

)
