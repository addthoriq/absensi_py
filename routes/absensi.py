from fastapi import APIRouter, Depends
from common.security import oauth2_scheme, get_user_from_jwt_token
from models import get_db_sync