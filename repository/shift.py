from sqlalchemy.orm import Session
from sqlalchemy import select, func, and_
from models.Shift import Shift
from typing import Optional, List, Tuple
from datetime import datetime
from math import ceil

def list_paginate(
    db: Session,
    page: int = 1,
    page_size: int = 10,
    nama_shift: Optional[str] = None,
    jam_mulai: Optional[str] = None,
    jam_akhir: Optional[str] = None
) -> Tuple[List[Shift], int, int]:
    limit = page_size
    offset = (page - 1) * limit
    stmt = select(Shift)
    stmt_count = select(func.count(Shift.id))
    if nama_shift is not None:
        stmt = stmt.filter(Shift.nama_shift.ilike(f"%{nama_shift}%"))
        stmt_count = stmt_count.filter(Shift.nama_shift.ilike(f"%{nama_shift}%"))
    if jam_mulai and jam_akhir is not None:
        stmt = stmt.filter(
            and_(
                Shift.jam_mulai >= jam_mulai,
                Shift.jam_akhir <= jam_akhir,
            )
        )
        stmt_count = stmt_count.filter(
            and_(
                Shift.jam_mulai >= jam_mulai,
                Shift.jam_akhir <= jam_akhir,
            )
        )

    stmt = stmt.order_by(Shift.id.asc()).limit(limit=limit).offset(offset=offset)
    get_list = db.execute(stmt).scalars().all()
    num_data = db.execute(stmt_count).scalar()
    num_page = ceil(num_data / limit)
    return get_list, num_data, num_page

def get_by_id(
    db: Session,
    id: int,
) -> Shift:
    query = select(Shift).filter(Shift.id == id)
    result = db.execute(query).scalar()
    return result

def create(
    db: Session,
    nama_shift: str,
    jam_mulai: str,
    jam_akhir: str,
    is_commit: bool = True
) -> Shift:
    new_data = Shift(
        nama_shift=nama_shift,
        jam_mulai=datetime.strptime(jam_mulai, "%H:%M:%S").time(),
        jam_akhir=datetime.strptime(jam_akhir, "%H:%M:%S").time()
    )
    db.add(new_data)
    if is_commit:
        db.commit()
    return new_data

def update(
    db: Session,
    id: int,
    nama_shift: str,
    jam_mulai: str,
    jam_akhir: str,
    is_commit: bool = True
) -> Shift:
    query = select(Shift).filter(Shift.id == id)
    data = db.execute(query).scalar()
    data.nama_shift=nama_shift
    data.jam_mulai=datetime.strptime(jam_mulai, "%H:%M:%S").time(),
    data.jam_akhir=datetime.strptime(jam_akhir, "%H:%M:%S").time()
    db.add(data)
    if is_commit:
        db.commit()
    return data

def delete(
    db: Session,
    id: int,
    is_commit: bool = True
) -> None:
    query = db.query(Shift).filter(Shift.id == id).first()
    db.delete(query)
    if is_commit:
        db.commit()
    return None