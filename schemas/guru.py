from pydantic import BaseModel

class PaginateGuruResponse(BaseModel):
    counts: int
    page_count: int
    page_size: int
    page: int
    
    class DetailGuruResponse(BaseModel)