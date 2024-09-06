from typing import List
from pydantic import BaseModel


class PaginateKehadiranResponse(BaseModel):
    count: int
    page_count: int
    page_size: int
    page: int

    class DetailKehadiranResponse(BaseModel):
        id: int
        nama_kehadiran: str
        keterangan: str

    result: List[DetailKehadiranResponse]


class DetailKehadiranResponse(BaseModel):
    id: int
    nama_kehadiran: str
    keterangan: str


class CreateKehadiranRequest(BaseModel):
    nama_kehadiran: str
    keterangan: str


class CreateKehadiranResponse(BaseModel):
    id: int
    nama_kehadiran: str
    keterangan: str


class UpdateKehadiranRequest(BaseModel):
    nama_kehadiran: str
    keterangan: str


class UpdateKehadiranResponse(BaseModel):
    id: int
    nama_kehadiran: str
    keterangan: str
