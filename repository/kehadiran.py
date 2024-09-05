from sqlalchemy.orm import Session
from models.Kehadiran import Kehadiran
from typing import Tuple, List, Optional
from math import ceil
from sqlalchemy import select, func

def paginate_list(
    db: Session,
    page: int = 1,
    page_size: int = 10,
    nama_kehadiran: Optional[str] = None,
) -> Tuple[List[Kehadiran], int, int]:
    limit = page_size
    offset = (page - 1) * limit
    stmt = select(Kehadiran)
    stmt_count = select(func.count(Kehadiran.id))
    if nama_kehadiran is not None:
        stmt = stmt.filter(Kehadiran.nama_kehadiran.ilike(f"%{nama_kehadiran}%"))
        stmt_count = stmt_count.filter(Kehadiran.nama_kehadiran.ilike(f"%{nama_kehadiran}%"))

    stmt = stmt.order_by(Kehadiran.id.asc()).limit(limit=limit).offset(offset=offset)
    get_list = db.execute(stmt).scalars().all()
    num_data = db.execute(stmt_count).scalar()
    num_page = ceil(num_data / limit)
    return get_list, num_data, num_page

def get_by_id(
    db: Session,
    id: int
) -> Kehadiran:
    query = select(Kehadiran).filter(Kehadiran.id == id)
    return db.execute(query).scalar()

def create(
    db: Session,
    nama_kehadiran: str,
    keterangan: str,
    is_commit: bool = True
) -> Kehadiran:
    new_data = Kehadiran(
        nama_kehadiran=nama_kehadiran,
        keterangan=keterangan
    )
    db.add(new_data)
    if is_commit:
        db.commit()
    return new_data

def update(
    db: Session,
    id: int,
    nama_kehadiran: str,
    keterangan: str,
    is_commit: bool = True
) -> Kehadiran:
    query = select(Kehadiran).filter(Kehadiran.id == id)
    data = db.execute(query).scalar()
    data.nama_kehadiran = nama_kehadiran
    data.keterangan = keterangan
    db.add(data)
    if is_commit:
        db.commit()
    return data

def delete(
    db: Session,
    id: int,
    is_commit: bool = True
) -> None:
    query = db.query(Kehadiran).filter(Kehadiran.id == id).first()
    db.delete(query)
    if is_commit:
        db.commit()
    return None