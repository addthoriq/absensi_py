from sqlalchemy.orm import Session
from models.Role import Role
from sqlalchemy import select, func
from typing import Optional, Tuple, List
from math import ceil

def paginate_jabatan(
    db: Session,
    page: int = 1,
    page_size: int = 10,
    jabatan: Optional[str] = None
) -> Tuple[List[Role], int, int]:
    limit = page_size
    offset = (page - 1) * limit
    stmt = select(Role)
    stmt_count = select(func.count(Role.id))
    if jabatan is not None:
        stmt = stmt.filter(Role.jabatan.ilike(f"%{jabatan}%"))
        stmt_count = stmt_count.filter(Role.jabatan.ilike(f"%{jabatan}%"))
    stmt = stmt.order_by(Role.id.asc()).limit(limit=limit).offset(offset=offset)
    get_list = db.execute(stmt).scalars().all()
    num_data = db.execute(stmt_count).scalar()
    num_page = ceil(num_data / limit)
    return get_list, num_data, num_page

def get_jabatan_by_id(
    db: Session,
    id: int
) -> Role:
    query = select(Role).filter(Role.id == id)
    return db.execute(query).scalar()

def create(
    db: Session,
    nama_jabatan: str,
    is_commit: bool = True
) -> Role:
    new_jabatan=Role(
        jabatan=nama_jabatan
    )
    db.add(new_jabatan)
    if is_commit:
        db.commit()
    return new_jabatan

def update(
    db: Session,
    id: int,
    nama_jabatan: str,
    is_commit: bool = True
) -> Role:
    query = select(Role).filter(Role.id == id)
    data = db.execute(query).scalar()
    data.jabatan = nama_jabatan
    db.add(data)
    if is_commit:
        db.commit()
    return data

def delete(
    db: Session,
    id: int,
    is_commit: bool = True
) -> None:
    query = db.query(Role).filter(Role.id == id).first()
    db.delete(query)
    if is_commit:
        db.commit()
    return None