from fastapi import APIRouter, Depends
from typing import Optional
from models import get_db_sync
from sqlalchemy.orm import Session
from common.security import oauth2_scheme, get_user_from_jwt_token
from repository import kehadiran as kehadiran_repo
from common.responses import (
    common_response,
    Ok,
    Created,
    InternalServerError,
    NoContent,
    NotFound,
    BadRequest,
    Unauthorized,
    Forbidden
)
from schemas.common import (
    NoContentResponse,
    InternalServerErrorResponse,
    NotFoundResponse,
    BadRequestResponse,
    UnauthorizedResponse,
    ForbiddenResponse
)
from schemas.kehadiran import (
    PaginateKehadiranResponse,
    DetailKehadiranResponse,
    CreateKehadiranRequest,
    CreateKehadiranResponse,
    UpdateKehadiranRequest,
    UpdateKehadiranResponse
)

router = APIRouter(prefix="/kehadiran", tags=["Kehadiran"])
MSG_UNAUTHORIZED = "Invalid/Expire credentials"

@router.get(
    "/",
    responses={
        "200": {"model": PaginateKehadiranResponse},
        "400": {"model": BadRequestResponse},
        "401": {"model": UnauthorizedResponse},
        "403": {"model": ForbiddenResponse},
        "500": {"model": InternalServerErrorResponse},
    }
)
async def get_paginate_list_kehadiran(
    nama_kehadiran: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db_sync),
    token: str = Depends(oauth2_scheme)
):
    try:
        user = get_user_from_jwt_token(db, token)
        if user is None:
            return common_response(Unauthorized(custom_response=MSG_UNAUTHORIZED))
        (data, num_data, num_page) = kehadiran_repo.paginate_list(
            db=db,
            page=page,
            page_size=page_size,
            nama_kehadiran=nama_kehadiran
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
                            "nama_kehadiran": val.nama_kehadiran,
                            "keterangan": val.keterangan
                        }
                        for val in data
                    ]
                }
            )
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return common_response(InternalServerError(error=str(e)))

@router.get(
    "/{id}",
    responses={
        "200": {"model": DetailKehadiranResponse},
        "400": {"model": BadRequestResponse},
        "401": {"model": UnauthorizedResponse},
        "403": {"model": ForbiddenResponse},
        "404": {"model": NotFoundResponse},
        "500": {"model": InternalServerErrorResponse},
    }
)
async def get_detail_kehadiran(
    id: int,
    db: Session = Depends(get_db_sync),
    token: str = Depends(oauth2_scheme)
):
    try:
        user = get_user_from_jwt_token(db, token)
        if user is None:
            return common_response(Unauthorized(custom_response=MSG_UNAUTHORIZED))
        data = kehadiran_repo.get_by_id(db, id)
        if data is None:
            return common_response(NotFound())
        return common_response(
            Ok(
                data={
                    "id": data.id,
                    "nama_kehadiran": data.nama_kehadiran,
                    "keterangan": data.keterangan
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
        "201": {"model": CreateKehadiranResponse},
        "400": {"model": BadRequestResponse},
        "401": {"model": UnauthorizedResponse},
        "403": {"model": ForbiddenResponse},
        "500": {"model": InternalServerErrorResponse},
    }
)
async def create_kehadiran(
    req: CreateKehadiranRequest,
    db: Session = Depends(get_db_sync),
    token: str = Depends(oauth2_scheme)
):
    try:
        user = get_user_from_jwt_token(db, token)
        if user is None:
            return common_response(Unauthorized(custom_response=MSG_UNAUTHORIZED))
        data = kehadiran_repo.create(
            db=db,
            nama_kehadiran=req.nama_kehadiran,
            keterangan=req.keterangan
        )
        return common_response(
            Created(
                data={
                    "id": data.id,
                    "nama_kehadiran": data.nama_kehadiran,
                    "keterangan": data.keterangan,
                }
            )
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return common_response(InternalServerError(error=str(e)))

@router.put(
    "/{id}",
    responses={
        "200": {"model": UpdateKehadiranResponse},
        "400": {"model": BadRequestResponse},
        "401": {"model": UnauthorizedResponse},
        "403": {"model": ForbiddenResponse},
        "404": {"model": NotFoundResponse},
        "500": {"model": InternalServerErrorResponse},
    }
)
async def update_kehadiran(
    id: int,
    req: UpdateKehadiranRequest,
    db: Session = Depends(get_db_sync),
    token: str = Depends(oauth2_scheme)
):
    try:
        user = get_user_from_jwt_token(db, token)
        if user is None:
            return common_response(Unauthorized(custom_response=MSG_UNAUTHORIZED))
        data = kehadiran_repo.get_by_id(db, id)
        if data is None:
            return common_response(NotFound())
        data = kehadiran_repo.update(
            db=db,
            id=id,
            nama_kehadiran=req.nama_kehadiran,
            keterangan=req.keterangan
        )
        return common_response(
            Ok(
                data={
                    "id": data.id,
                    "nama_kehadiran": data.nama_kehadiran,
                    "keterangan": data.keterangan
                }
            )
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return common_response(InternalServerError(error=str(e)))

@router.delete(
    "/{id}",
    responses={
        "204": {"model": NoContentResponse},
        "400": {"model": BadRequestResponse},
        "401": {"model": UnauthorizedResponse},
        "403": {"model": ForbiddenResponse},
        "404": {"model": NotFoundResponse},
        "500": {"model": InternalServerErrorResponse},
    }
)
async def delete_kehadiran(
    id: int,
    db: Session = Depends(get_db_sync),
    token: str = Depends(oauth2_scheme)
):
    try:
        user = get_user_from_jwt_token(db, token)
        if user is None:
            return common_response(Unauthorized(custom_response=MSG_UNAUTHORIZED))
        data = kehadiran_repo.get_by_id(db, id)
        if data is None:
            return common_response(NotFound())
        kehadiran_repo.delete(db, id)
        return common_response(
            NoContent()
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return common_response(InternalServerError(error=str(e)))