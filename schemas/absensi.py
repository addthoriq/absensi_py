from typing import List
from pydantic import BaseModel


class PaginateAbsensiResponse(BaseModel):
    count: int
    page_count: int
    page_size: int
    page: int

    class DetailAbsensiResponse(BaseModel):
        id: int
        tanggal_absen: str
        jam_masuk: str
        jam_keluar: str
        keterangan: str
        lokasi: str

        class GetUserDetail(BaseModel):
            id: int
            nama_user: str
            email: str

            class GetJabatanUser(BaseModel):
                id: int
                nama_jabatan: str

            jabatan: List[GetJabatanUser]

        class GetShiftDetail(BaseModel):
            id: int
            nama_shift: str
            jam_mulai: str
            jam_akhir: str

        class GetKehadiranDetail(BaseModel):
            id: int
            nama_kehadiran: str
            keterangan: str

        user: List[GetUserDetail]
        shift: List[GetShiftDetail]
        kehadiran: List[GetKehadiranDetail]


class DetailAbsensiResponse(BaseModel):
    id: int
    tanggal_absen: str
    jam_masuk: str
    jam_keluar: str
    keterangan: str
    lokasi: str

    class GetUserDetail(BaseModel):
        id: int
        nama_user: str
        email: str

        class GetJabatanUser(BaseModel):
            id: int
            nama_jabatan: str

        jabatan: List[GetJabatanUser]

    class GetShiftDetail(BaseModel):
        id: int
        nama_shift: str
        jam_mulai: str
        jam_akhir: str

    class GetKehadiranDetail(BaseModel):
        id: int
        nama_kehadiran: str
        keterangan: str

    user: List[GetUserDetail]
    shift: List[GetShiftDetail]
    kehadiran: List[GetKehadiranDetail]


class CreateAbsensiRequest(BaseModel):
    tanggal_absen: str
    jam_masuk: str
    jam_keluar: str
    lokasi: str
    keterangan: str
    user_id: int
    shift_id: int
    kehadiran_id: int


class CreateAbsensiResponse(BaseModel):
    tanggal_absen: str
    jam_masuk: str
    jam_keluar: str
    lokasi: str
    keterangan: str

    class GetUserDetail(BaseModel):
        id: int
        nama_user: str
        email: str

        class GetJabatanUser(BaseModel):
            id: int
            nama_jabatan: str

        jabatan: List[GetJabatanUser]

    class GetShiftDetail(BaseModel):
        id: int
        nama_shift: str
        jam_mulai: str
        jam_akhir: str

    class GetKehadiranDetail(BaseModel):
        id: int
        nama_kehadiran: str
        keterangan: str

    user: List[GetUserDetail]
    shift: List[GetShiftDetail]
    kehadiran: List[GetKehadiranDetail]
