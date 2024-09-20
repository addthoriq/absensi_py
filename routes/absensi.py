from fastapi import APIRouter, Depends, Request
from typing import Optional
from sqlalchemy.orm import Session
from common.security import oauth2_scheme, get_user_from_jwt_token
from models import get_db_sync
from repository import absensi as absensi_repo
from common.responses import (
    common_response,
    Ok,
    Created,
    InternalServerError,
    NotFound,
    NoContent,
    Unauthorized
)
from schemas.common import (
    NoContentResponse,
    NotFoundResponse,
    InternalServerErrorResponse,
    UnauthorizedResponse,
    BadRequestResponse
)
from schemas.absensi import (
    CreateAbsensiRequest,
    CreateAbsensiResponse,
    PaginateAbsensiResponse,
    DetailAbsensiResponse,
    GetAbsensiByCurrentUser,
    UpdateAbsensiJamKeluarRequest,
    UpdateAbsensiJamKeluarResponse
)

router = APIRouter(prefix="/absensi", tags=["Absensi"])
MSG_UNAUTHORIZED = "Invalid/Expired Credentials"

@router.get(
    "/",
    responses={
        "200": {"model": PaginateAbsensiResponse},
        "400": {"model": BadRequestResponse},
        "401": {"model": UnauthorizedResponse},
        "500": {"model": InternalServerErrorResponse},
    }
)
async def paginate_list_absensi(
    db: Session = Depends(get_db_sync),
    token: str = Depends(oauth2_scheme),
    page: int = 1,
    page_size: int = 10,
    tanggal_absen: Optional[str] = None,
    user_name: Optional[str] = None,
    jam_masuk: Optional[str] = None,
    jam_keluar: Optional[str] = None,
):
    try:
        user = get_user_from_jwt_token(db, token)
        if user is None:
            return common_response(Unauthorized(custom_response=MSG_UNAUTHORIZED))
        (data, num_data, num_page) = absensi_repo.paginate_list(
            db=db,
            page=page,
            page_size=page_size,
            tanggal_absen=tanggal_absen,
            user_name=user_name,
            jam_masuk=jam_masuk,
            jam_keluar=jam_keluar
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
                            "tanggal_absen": val.tanggal_absen,
                            "jam_masuk": val.jam_masuk,
                            "jam_keluar": val.jam_keluar if val.jam_keluar else None,
                            "keterangan": val.keterangan,
                            "lokasi": val.lokasi,
                            "shift": {
                                "id": val.absen_shift.id,
                                "nama_shift": val.absen_shift.nama_shift,
                                "jam_mulai": val.absen_shift.jam_mulai,
                                "jam_akhir": val.absen_shift.jam_akhir
                            } if val.absen_shift else None,
                            "kehadiran": {
                                "id": val.absen_kehadiran.id,
                                "nama_kehadiran": val.absen_kehadiran.nama_kehadiran,
                                "keterangan": val.absen_kehadiran.keterangan,
                            } if val.absen_kehadiran else None,
                            "user":{
                                "id": val.absen_user.id,
                                "nama_user": val.absen_user.nama_user,
                                "email": val.absen_user.email,
                                "jabatan": {
                                    "id": val.absen_user.userRole.id,
                                    "nama_jabatan": val.absen_user.userRole.jabatan
                                } if val.absen_user.userRole else None
                            } if val.absen_user else None
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
        "200": {"model": DetailAbsensiResponse},
        "400": {"model": BadRequestResponse},
        "401": {"model": UnauthorizedResponse},
        "404": {"model": NotFoundResponse},
        "500": {"model": InternalServerErrorResponse},
    }
)
async def get_detail_absensi(
    id: int,
    db: Session = Depends(get_db_sync),
    token: str = Depends(oauth2_scheme)
):
    try:
        user = get_user_from_jwt_token(db, token)
        if user is None:
            return common_response(Unauthorized(custom_response=MSG_UNAUTHORIZED))
        data = absensi_repo.get_by_id(db, id)
        if data is None:
            return common_response(NotFound())
        return common_response(
            Ok(
                data={
                    "id": data.id,
                    "tanggal_absen": data.tanggal_absen,
                    "jam_masuk": data.jam_masuk,
                    "jam_keluar": data.jam_keluar if data.jam_keluar else None,
                    "keterangan": data.keterangan,
                    "lokasi": data.lokasi,
                    "shift": {
                        "id": data.absen_shift.id,
                        "nama_shift": data.absen_shift.nama_shift,
                        "jam_mulai": data.absen_shift.jam_mulai,
                        "jam_akhir": data.absen_shift.jam_akhir,
                    } if data.absen_shift else None,
                    "kehadiran": {
                        "id": data.absen_kehadiran.id,
                        "nama_kehadiran": data.absen_kehadiran.nama_kehadiran,
                        "keterangan": data.absen_kehadiran.keterangan
                    } if data.absen_kehadiran else None,
                    "user": {
                        "id": data.absen_user.id,
                        "nama_user": data.absen_user.nama,
                        "email": data.absen_user.email,
                        "jabatan": {
                            "id": data.absen_user.userRole.id,
                            "nama_jabatan": data.absen_user.userRole.jabatan
                        } if data.absen_user.userRole else None
                    } if data.absen_user else None
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
        "201": {"model": CreateAbsensiResponse},
        "400": {"model": BadRequestResponse},
        "401": {"model": UnauthorizedResponse},
        "500": {"model": InternalServerErrorResponse},
    }
)
async def create_absensi(
    req: CreateAbsensiRequest,
    r: Request,
    db: Session = Depends(get_db_sync),
    token: str = Depends(oauth2_scheme)
):
    try:
        ip_address = r.headers.get("x-real-ip", r.client.host)
        user = get_user_from_jwt_token(db, token)
        if user is None:
            return common_response(Unauthorized(MSG_UNAUTHORIZED))
        
        data = absensi_repo.create(
            db=db,
            keterangan=req.keterangan,
            lokasi=ip_address,
            userId=user,
            kehadiran_id=req.kehadiran_id,
            shift_id=req.shift_id
        )
        return common_response(
            Ok(
                data={
                    "id": data.id,
                    "tanggal_absen": data.tanggal_absen,
                    "jam_masuk": data.jam_masuk,
                    "lokasi": data.lokasi,
                    "keterangan": data.keterangan,
                    "shift": {
                        "id": data.absen_shift.id,
                        "nama_shift": data.absen_shift.nama_shift,
                        "jam_mulai": data.absen_shift.jam_mulai,
                        "jam_keluar": data.absen_shift.jam_keluar
                    } if data.absen_shift else None,
                    "kehadiran": {
                        "id": data.absen_kehadiran.id,
                        "nama_kehadiran": data.absen_kehadiran.nama_kehadiran,
                        "keterangan": data.absen_kehadiran.keterangan
                    } if data.absen_kehadiran else None,
                    "user": {
                        "id": data.absen_user.id,
                        "nama_user": data.absen_user.nama,
                        "email": data.absen_user.email,
                        "jabatan": {
                            "id": data.absen_user.userRole.id,
                            "nama_jabatan": data.absen_user.userRole.jabatan
                        } if data.absen_user.userRole else None
                    } if data.absen_user else None
                }
            )
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return common_response(InternalServerError(error=str(e)))