from fastapi import Depends, APIRouter
from common.security import oauth2_scheme, get_user_from_jwt_token
from models import get_db_sync
from datetime import datetime
from sqlalchemy.orm import Session
from typing import Optional
from repository import shift as shift_repo
from common.responses import (
    common_response,
    Ok,
    NoContent,
    NotFound,
    BadRequest,
    InternalServerError,
    Unauthorized,
    Forbidden,
    Created
)
from schemas.common import (
    NoContentResponse,
    NotFoundResponse,
    BadRequestResponse,
    InternalServerErrorResponse,
    UnauthorizedResponse,
    ForbiddenResponse,
)
from schemas.shift import (
    CreateShiftRequest,
    CreateShiftResponse,
    UpdateShiftRequest,
    UpdateShiftResponse,
    PaginateShiftResponse,
    DetailShiftResponse,
)

router = APIRouter(prefix="/shift", tags=["Shift"])
MSG_UNAUTHORIZED="Invalid/Expired Credentials"

@router.get(
    "/",
    responses={
        "200": {"model": PaginateShiftResponse},
        "400": {"model": BadRequestResponse},
        "401": {"model": UnauthorizedResponse},
        "403": {"model": ForbiddenResponse},
        "500": {"model": InternalServerErrorResponse}
    }
)
async def get_paginate_shift(
    page: int = 1,
    page_size: int = 10,
    nama_shift: Optional[str] = None,
    jam_mulai: Optional[str] = None,
    jam_akhir: Optional[str] = None,
    db: Session = Depends(get_db_sync),
    token: str = Depends(oauth2_scheme),
):
    try:
        user = get_user_from_jwt_token(db, token)
        if user is None:
            return common_response(Unauthorized(custom_response=MSG_UNAUTHORIZED))
        (data, num_data, num_page) = shift_repo.list_paginate(
            db=db,
            page=page,
            page_size=page_size,
            nama_shift=nama_shift,
            jam_mulai=jam_mulai,
            jam_akhir=jam_akhir
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
                            "nama_shift": val.nama_shift,
                            "jam_mulai": str(val.jam_mulai),
                            "jam_akhir": str(val.jam_akhir)
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
        "200": {"model": DetailShiftResponse},
        "400": {"model": BadRequestResponse},
        "401": {"model": UnauthorizedResponse},
        "403": {"model": ForbiddenResponse},
        "404": {"model": NotFoundResponse},
        "500": {"model": InternalServerErrorResponse}
    }
)
async def get_detail_shift(
    id: int,
    db: Session = Depends(get_db_sync),
    token: str = Depends(oauth2_scheme),
):
    try:
        user = get_user_from_jwt_token(db, token)
        if user is None:
            return common_response(Unauthorized(custom_response=MSG_UNAUTHORIZED))
        data = shift_repo.get_by_id(db, id)
        if data is None:
            return common_response(NotFound())
        return common_response(
            Ok(
                data={
                    "id": data.id,
                    "nama_shift": data.nama_shift,
                    "jam_mulai": data.jam_mulai,
                    "jam_akhir": data.jam_akhir
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
        "201": {"model": CreateShiftResponse},
        "400": {"model": BadRequestResponse},
        "401": {"model": UnauthorizedResponse},
        "403": {"model": ForbiddenResponse},
        "500": {"model": InternalServerErrorResponse}
    }
)
async def create_shift(
    req: CreateShiftRequest,
    db: Session = Depends(get_db_sync),
    token: str = Depends(oauth2_scheme)
):
    try:
        user = get_user_from_jwt_token(db, token)
        if user is None:
            return common_response(Unauthorized(custom_response=MSG_UNAUTHORIZED))
        data = shift_repo.create(
            db=db,
            nama_shift=req.nama_shift,
            jam_mulai=req.jam_mulai,
            jam_akhir=req.jam_akhir,
        )
        return common_response(
            Created(
                data={
                    "id": data.id,
                    "nama_shift": data.nama_shift,
                    "jam_mulai": datetime.strptime(data.jam_mulai, "%H:%M:%S").time(),
                    "jam_akhir": datetime.strptime(data.jam_akhir, "%H:%M:%S").time(),
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
        "200": {"model": UpdateShiftResponse},
        "400": {"model": BadRequestResponse},
        "401": {"model": UnauthorizedResponse},
        "403": {"model": ForbiddenResponse},
        "404": {"model": NotFoundResponse},
        "500": {"model": InternalServerErrorResponse}
    }
)
async def update_shift(
    id: str,
    req: UpdateShiftRequest,
    db: Session = Depends(get_db_sync),
    token: str = Depends(oauth2_scheme)
):
    try:
        user = get_user_from_jwt_token(db, token)
        if user is None:
            return common_response(Unauthorized(custom_response=MSG_UNAUTHORIZED))
        data = shift_repo.get_by_id(db, id)
        if data is None:
            return common_response(NotFound())
        data = shift_repo.update(
            db=db,
            id=id,
            nama_shift=req.nama_shift,
            jam_mulai=req.jam_mulai,
            jam_akhir=req.jam_akhir
        )
        return common_response(
            Ok(
                data={
                    "id": data.id,
                    "nama_shift": data.nama_shift,
                    "jam_mulai": datetime.strptime(data.jam_mulai, "%H:%M:%S").time(),
                    "jam_akhir": datetime.strptime(data.jam_akhir, "%H:%M:%S").time(),
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
        "500": {"model": InternalServerErrorResponse}
    }
)
async def delete_shift(
    id: int,
    db: Session = Depends(get_db_sync),
    token: str = Depends(oauth2_scheme)
):
    try:
        user = get_user_from_jwt_token(db, token)
        if user is None:
            return common_response(Unauthorized(custom_response=MSG_UNAUTHORIZED))
        data = shift_repo.get_by_id(db, id)
        if data is None:
            return common_response(NotFound())
        shift_repo.delete(
            db=db,
            id=id
        )
        return common_response(NoContent())
    except Exception as e:
        import traceback
        traceback.print_exc()
        return common_response(InternalServerError(error=str(e)))