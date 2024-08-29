from fastapi import Depends, APIRouter
from typing import Optional
from sqlalchemy.orm import Session
from common.security import oauth2_scheme, get_user_from_jwt_token
from models import get_db_sync
from repository import jabatan as jabatan_repo
from common.responses import (
    common_response,
    BadRequest,
    Forbidden,
    Ok,
    NoContent,
    InternalServerError,
    Created,
    NotFound,
    Unauthorized,
)
from schemas.common import (
    BadRequestResponse,
    ForbiddenResponse,
    NoContentResponse,
    InternalServerErrorResponse,
    UnauthorizedResponse,
    NotFoundResponse
)
from schemas.jabatan import (
    PaginateRoleResponse,
    CreateJabatanRequest,
    CreateJabatanResponse,
    UpdateJabatanRequest,
    UpdateJabatanResponse,
    DetailJabatanResponse,
)

router = APIRouter(prefix="/jabatan", tags=["Jabatan"])
MSG_UNAUTHORIZED="Invalid/Expire Credentials"

@router.get(
    "/",
    responses={
        "200": {"model": PaginateRoleResponse},
        "400": {"model": BadRequestResponse},
        "401": {"model": UnauthorizedResponse},
        "403": {"model": ForbiddenResponse},
        "500": {"model": InternalServerErrorResponse}
    }
)
async def paginate_list(
    db: Session = Depends(get_db_sync),
    token: str = Depends(oauth2_scheme),
    page: int = 1,
    page_size: int = 10,
    nama_jabatan: Optional[str] = None,
):
    try:
        user = get_user_from_jwt_token(db, token)
        if user is None:
            return common_response(Unauthorized(custom_response=MSG_UNAUTHORIZED))
        (data, num_data, num_page) = jabatan_repo.paginate_jabatan(
            db=db,
            page=page,
            page_size=page_size,
            jabatan=nama_jabatan
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
                            "nama_jabatan": val.jabatan
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
        "200": {"model": DetailJabatanResponse},
        "400": {"model": BadRequestResponse},
        "404": {"model": NotFoundResponse},
        "401": {"model": UnauthorizedResponse},
        "403": {"model": ForbiddenResponse},
        "500": {"model": InternalServerErrorResponse}
    }
)
async def get_detail(
    id: int,
    db: Session = Depends(get_db_sync),
    token: str = Depends(oauth2_scheme)
):
    try:
        user = get_user_from_jwt_token(db, token)
        if user is None:
            return common_response(Unauthorized(custom_response=MSG_UNAUTHORIZED))
        data = jabatan_repo.get_jabatan_by_id(db=db, id=id)
        if data is None:
            return common_response(NotFound())
        return common_response(
            Ok(
                data={
                    "id": data.id,
                    "nama_jabatan": data.jabatan
                }
            )
        )
    except Exception as e:
        import traceback
        traceback.print_exc
        return common_response(InternalServerError(error=str(e)))

@router.post(
    "/",
    responses={
        "201": {"model": CreateJabatanResponse},
        "400": {"model": BadRequestResponse},
        "401": {"model": UnauthorizedResponse},
        "403": {"model": ForbiddenResponse},
        "500": {"model": InternalServerErrorResponse}
    }
)
async def create_jabatan(
    req: CreateJabatanRequest,
    db: Session = Depends(get_db_sync),
    token: str = Depends(oauth2_scheme)
):
    try:
        user = get_user_from_jwt_token(db, token)
        if user is None:
            return common_response(Unauthorized(custom_response=MSG_UNAUTHORIZED))
        data = jabatan_repo.create(
            db=db,
            nama_jabatan=req.nama_jabatan
        )
        return common_response(
            Created(
                data={
                    "id": data.id,
                    "nama_jabatan": data.jabatan
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
        "200": {"model": UpdateJabatanResponse},
        "400": {"model": BadRequestResponse},
        "404": {"model": NotFoundResponse},
        "401": {"model": UnauthorizedResponse},
        "403": {"model": ForbiddenResponse},
        "500": {"model": InternalServerErrorResponse}
    }
)
async def update_jabatan(
    id: int,
    req: UpdateJabatanRequest,
    db: Session = Depends(get_db_sync),
    token: str = Depends(oauth2_scheme)
):
    try:
        user = get_user_from_jwt_token(db, token)
        if user is None:
            return common_response(Unauthorized(custom_response=MSG_UNAUTHORIZED))
        data = jabatan_repo.get_jabatan_by_id(db, id)
        if data is None:
            return common_response(NotFound())
        result = jabatan_repo.update(
            db=db,
            id=id,
            nama_jabatan=req.nama_jabatan
        )
        return common_response(
            Ok(
                data={
                    "id": result.id,
                    "nama_jabatan": result.jabatan
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
        "404": {"model": NotFoundResponse},
        "401": {"model": UnauthorizedResponse},
        "403": {"model": ForbiddenResponse},
        "500": {"model": InternalServerErrorResponse}
    }
)
async def delete_jabatan(
    id: int,
    db: Session = Depends(get_db_sync),
    token: str = Depends(oauth2_scheme)
):
    try:
        user = get_user_from_jwt_token(db, token)
        if user is None:
            return common_response(Unauthorized(custom_response=MSG_UNAUTHORIZED))
        data = jabatan_repo.get_jabatan_by_id(db, id)
        if data is None:
            return common_response(NotFound())
        jabatan_repo.delete(db, id)
        return common_response(
            NoContent()
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return common_response(InternalServerError(error=str(e)))