from typing import List
from pydantic import BaseModel

class PaginateShiftResponse(BaseModel):
    counts: int
    page_count: int
    page_size: int
    page: int
    
    class DetailShiftResponse(BaseModel):
        id: int
        nama_shift: str
        jam_mulai: str
        jam_akhir: str
        
    result: List[DetailShiftResponse]
    
class DetailShiftResponse(BaseModel):
    id: int
    nama_shift: str
    jam_mulai: str
    jam_akhir: str

class CreateShiftRequest(BaseModel):
    nama_shift: str
    jam_mulai: str
    jam_akhir: str

class CreateShiftResponse(BaseModel):
    id: int
    nama_shift: str
    jam_mulai: str
    jam_akhir: str

class UpdateShiftRequest(BaseModel):
    nama_shift: str
    jam_mulai: str
    jam_akhir: str
    
class UpdateShiftResponse(BaseModel):
    id: int
    nama_shift: str
    jam_mulai: str
    jam_akhir: str