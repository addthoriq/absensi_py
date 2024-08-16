from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from common.responses import (
    common_response,
    BadRequest,
    InternalServerError,
    Ok,
    Unauthorized,
)
from common.security import (
    generate_jwt_token_from_user,
    get_user_from_jwt_token,
    oauth2_scheme,
)
from models import get_db_sync
from schemas.common import (
    UnauthorizedResponse,
    BadRequestResponse,
    InternalServerErrorResponse,
)
from schemas.auth import (
    LoginRequest,
    LoginSuccessResponse,
    MeSuccessResponse,
)
from repository import auth as auth_repo

router = APIRouter(prefix="/auth", tags=["Auth"])
MSG_NotValidUser = "Invalid Credentials"


@router.post(
    "/login",
    responses={
        "200": {"model": LoginSuccessResponse},
        "400": {"model": BadRequestResponse},
        "500": {"model": InternalServerErrorResponse},
    },
)
async def login(req: LoginRequest, db: Session = Depends(get_db_sync)):
    try:
        is_valid = auth_repo.check_user_password(
            db=db, email=req.email, password=req.password
        )
        if not is_valid:
            return common_response(BadRequest(message=MSG_NotValidUser))
        user = auth_repo.get_user_by_email(db=db, email=req.email)
        token = await generate_jwt_token_from_user(user=user)
        return common_response(
            Ok(
                data={
                    "id": user.id,
                    "email": user.email,
                    "nama": user.nama,
                    "token": token,
                }
            )
        )

    except Exception as e:
        import traceback

        traceback.print_exc()
        return common_response(InternalServerError(error=str(e)))


@router.post("/token/")
async def generate_token(
    db: Session = Depends(get_db_sync), form_data: OAuth2PasswordRequestForm = Depends()
):
    try:
        is_valid = auth_repo.check_user_password(
            db=db, email=form_data.username, password=form_data.password
        )
        if not is_valid:
            return common_response(BadRequest(message=MSG_NotValidUser))
        user = auth_repo.get_user_by_email(db=db, email=form_data.username)
        token = await generate_jwt_token_from_user(user=user)
        return {"access_token": token, "token_type": "Bearer"}

    except Exception as e:
        import traceback

        traceback.print_exc()
        return common_response(InternalServerError(error=str(e)))


@router.get(
    "/me",
    responses={
        "200": {"model": MeSuccessResponse},
        "400": {"model": BadRequestResponse},
        "401": {"model": UnauthorizedResponse},
        "500": {"model": InternalServerErrorResponse},
    },
)
async def me(db: Session = Depends(get_db_sync), token: str = Depends(oauth2_scheme)):
    try:
        user = get_user_from_jwt_token(db, token)
        if user is None:
            return common_response(Unauthorized())
        return common_response(
            Ok(
                data={
                    "id": user.id,
                    "email": user.email,
                    "nama": user.nama,
                    "jabatan": {
                        "id": user.userRole.id,
                        "nama_jabatan": user.userRole.jabatan,
                    },
                }
            )
        )
    except Exception as e:
        import traceback

        traceback.print_exc()
        return common_response(InternalServerError(error=str(e)))
