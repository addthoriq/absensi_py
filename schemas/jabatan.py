from typing import List
from pydantic import BaseModel


class PaginateRoleResponse(BaseModel):
    count: int
    page_count: int
    page_size: int
    page: int

    class DetailRoleResponse(BaseModel):
        id: int
        nama_jabatan: str

    jabatan: List[DetailRoleResponse]


class DetailJabatanResponse(BaseModel):
    id: int
    nama_jabatan: str


class CreateJabatanRequest(BaseModel):
    nama_jabatan: str


class CreateJabatanResponse(BaseModel):
    id: int
    nama_jabatan: str


class UpdateJabatanRequest(BaseModel):
    nama_jabatan: str


class UpdateJabatanResponse(BaseModel):
    id: int
    nama_jabatan: str
