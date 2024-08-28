from fastapi import APIRouter, Depends
from typing import Optional
from sqlalchemy.orm import Session
from common.security import oauth2_scheme, get_user_from_jwt_token
from models import get_db_sync
from schemas.user import (
    PaginateUserResponse,
    CreateUserRequest,
    CreateUserResponse,
    UpdateUserRequest,
    UpdateUserResponse,
    DetailUserResponse,
)
from schemas.common import (
    BadRequestResponse,
    UnauthorizedResponse,
    NotFoundResponse,
    ForbiddenResponse,
    NoContentResponse,
    InternalServerErrorResponse,
)
from common.responses import (
    common_response,
    InternalServerError,
    Unauthorized,
    NotFound,
    NoContent,
    Created,
    Ok,
)
from repository import user as user_repo

router = APIRouter(prefix="/user-management", tags=["User Management"])
MSG_UNAUTHORIZED = "Invalid/Expired Credentials"


@router.get(
    "/",
    responses={
        "200": {"model": PaginateUserResponse},
        "400": {"model": BadRequestResponse},
        "401": {"model": UnauthorizedResponse},
        "403": {"model": ForbiddenResponse},
        "500": {"model": InternalServerErrorResponse},
    },
)
async def get_paginate_user(
    db: Session = Depends(get_db_sync),
    token: str = Depends(oauth2_scheme),
    page: int = 1,
    page_size: int = 10,
    nama_user: Optional[str] = None,
    email: Optional[str] = None,
    jabatan: Optional[int] = None,
):
    try:
        user = get_user_from_jwt_token(db, token)
        if user is None:
            return common_response(Unauthorized(custom_response=MSG_UNAUTHORIZED))
        (data, num_data, num_page) = user_repo.list_users(
            db=db,
            page=page,
            page_size=page_size,
            nama=nama_user,
            email=email,
            jabatan=jabatan,
        )
        return common_response(
            Ok(
                data={
                    "count": num_data,
                    "page_count": num_page,
                    "page_size": page_size,
                    "page": page,
                    "results": [
                        {
                            "id": val.id,
                            "email": val.email,
                            "nama_user": val.nama,
                            "jabatan": {
                                "id": val.userRole.id,
                                "nama_jabatan": val.userRole.jabatan,
                            }
                            if val.userRole
                            else None,
                        }
                        for val in data
                    ],
                }
            )
        )
    except Exception as e:
        import traceback

        traceback.print_exc()
        return common_response(InternalServerError(error=str(e)))


@router.get(
    "/{id}/",
    responses={
        "200": {"model": DetailUserResponse},
        "400": {"model": BadRequestResponse},
        "401": {"model": UnauthorizedResponse},
        "403": {"model": ForbiddenResponse},
        "404": {"model": NotFoundResponse},
        "500": {"model": InternalServerErrorResponse},
    },
)
async def get_detail_user(
    id: int, db: Session = Depends(get_db_sync), token: str = Depends(oauth2_scheme)
):
    try:
        user = get_user_from_jwt_token(db, token)
        if user is None:
            return common_response(Unauthorized(custom_response=MSG_UNAUTHORIZED))
        data = user_repo.get_user_by_id(db, id)
        if data is None:
            return common_response(NotFound())
        return common_response(
            Ok(
                data={
                    "id": data.id,
                    "email": data.email,
                    "nama_user": data.nama,
                    "jabatan": {
                        "id": data.userRole.id,
                        "nama_jabatan": data.userRole.jabatan,
                    },
                }
            )
        )
    except Exception as e:
        import traceback

        traceback.print_exc()
        return common_response(InternalServerError(error=str(e)))


@router.post(
    "/",
    responses={
        "201": {"model": CreateUserResponse},
        "400": {"model": BadRequestResponse},
        "401": {"model": UnauthorizedResponse},
        "403": {"model": ForbiddenResponse},
        "500": {"model": InternalServerErrorResponse},
    },
)
async def create_user(
    req: CreateUserRequest,
    db: Session = Depends(get_db_sync),
    token: str = Depends(oauth2_scheme),
):
    try:
        user = get_user_from_jwt_token(db, token)
        if user is None:
            return common_response(Unauthorized(custom_response=MSG_UNAUTHORIZED))
        data = user_repo.create_user(
            db=db,
            nama=req.nama_user,
            email=req.email,
            password=req.password,
            jabatan=req.jabatan,
        )
        return common_response(
            Created(
                data={
                    "id": data.id,
                    "nama_user": data.nama,
                    "email": data.email,
                    "jabatan": {
                        "id": data.userRole.id,
                        "nama_jabatan": data.userRole.jabatan,
                    },
                }
            )
        )
    except Exception as e:
        import traceback

        traceback.print_exc()
        return common_response(InternalServerError(error=str(e)))


@router.put(
    "/{id}/",
    responses={
        "200": {"model": UpdateUserResponse},
        "400": {"model": BadRequestResponse},
        "401": {"model": UnauthorizedResponse},
        "403": {"model": ForbiddenResponse},
        "404": {"model": NotFoundResponse},
        "500": {"model": InternalServerErrorResponse},
    },
)
async def update_user(
    id: int,
    req: UpdateUserRequest,
    db: Session = Depends(get_db_sync),
    token: str = Depends(oauth2_scheme),
):
    try:
        user = get_user_from_jwt_token(db, token)
        if user is None:
            return common_response(Unauthorized(custom_response=MSG_UNAUTHORIZED))
        check_data = user_repo.get_user_by_id(db, id)
        if check_data is None:
            return common_response(NotFound())
        data = user_repo.update_user(
            db=db,
            id=id,
            nama=req.nama_user,
            email=req.email,
            jabatan=req.jabatan,
        )
        return common_response(
            Ok(
                data={
                    "id": data.id,
                    "nama_user": data.nama,
                    "email": data.email,
                    "jabatan": {
                        "id": data.userRole.id,
                        "nama_jabatan": data.userRole.jabatan,
                    },
                }
            )
        )
    except Exception as e:
        import traceback

        traceback.print_exc()
        return common_response(InternalServerError(error=str(e)))


@router.delete(
    "/{id}/",
    responses={
        "204": {"model": NoContentResponse},
        "400": {"model": BadRequestResponse},
        "401": {"model": UnauthorizedResponse},
        "403": {"model": ForbiddenResponse},
        "404": {"model": NotFoundResponse},
        "500": {"model": InternalServerErrorResponse},
    },
)
async def delete_user(
    id: int, db: Session = Depends(get_db_sync), token: str = Depends(oauth2_scheme)
):
    try:
        user = get_user_from_jwt_token(db, token)
        if user is None:
            return common_response(Unauthorized(custom_response=MSG_UNAUTHORIZED))
        check_data = user_repo.get_user_by_id(db, id)
        if check_data is None:
            return common_response(NotFound())
        user_repo.delete_user(db, id)
        return common_response(NoContent())

    except Exception as e:
        import traceback

        traceback.print_exc()
        return common_response(InternalServerError(error=str(e)))
