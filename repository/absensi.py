from sqlalchemy.orm import Session
from sqlalchemy import select, func
from models.Absensi import Absensi
from math import ceil
from typing import Tuple, List, Optional
from datetime import datetime

def paginate_list(
    db: Session,
    page: int = 1,
    page_size: int = 10,
    tanggal_absen: Optional[str] = None,
    user_id: Optional[int] = None,
    kehadiran_id: Optional[int] = None
) -> Tuple[List[Absensi], int, int]:
    limit = page_size
    offset = (page - 1) * limit
    stmt = select(Absensi)
    stmt_count = select(func.count(Absensi.id))
    # if jabatan is not None:
    #     stmt = stmt.filter(Role.jabatan.ilike(f"%{jabatan}%"))
    #     stmt_count = stmt_count.filter(Role.jabatan.ilike(f"%{jabatan}%"))
    if tanggal_absen is not None:
        tanggal_absen = datetime.strptime(tanggal_absen, "yyyy-mm-dd").date()
        stmt = stmt.where(Absensi.tanggal_absen == tanggal_absen)
    stmt = stmt.order_by(Role.id.asc()).limit(limit=limit).offset(offset=offset)
    get_list = db.execute(stmt).scalars().all()
    num_data = db.execute(stmt_count).scalar()
    num_page = ceil(num_data / limit)
    return get_list, num_data, num_page