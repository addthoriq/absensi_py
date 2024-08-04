
from typing import List
from pydantic import BaseModel, field_validator

class PaginateAbsensiResponse(BaseModel):
    counts: int
    page_count: int
    page_size: int
    page: int
    
    class DetailAbsensiResponse(BaseModel):
        id: int
        tanggal_absen: str
        jam_masuk: str
        jam_keluar: str
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
        

class DetailAbsensiResponse(BaseModel):
    id: int
    tanggal_absen: str
    jam_masuk: str
    jam_keluar: str
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

# class CreateAbsensiRequest(BaseModel):
    