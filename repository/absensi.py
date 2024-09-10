from sqlalchemy.orm import Session
from sqlalchemy import select, func
from models.Absensi import Absensi
from models.User import User
from models.Kehadiran import Kehadiran
from models.Shift import Shift
from math import ceil
from typing import Tuple, List, Optional
from datetime import datetime

def paginate_list(
    db: Session,
    page: int = 1,
    page_size: int = 10,
    tanggal_absen: Optional[str] = None,
    user_name: Optional[str] = None,
    jam_masuk: Optional[str] = None,
    jam_keluar: Optional[str] = None
) -> Tuple[List[Absensi], int, int]:
    limit = page_size
    offset = (page - 1) * limit
    stmt = select(Absensi)
    stmt_count = select(func.count(Absensi.id))
    if user_name is not None:
        stmt = stmt.join(User).filter(User.nama.ilike(f"%{user_name}%"))
        stmt_count = stmt_count.join(User).filter(User.nama.ilike(f"%{user_name}%"))
    if tanggal_absen is not None:
        tanggal_absen = datetime.strptime(tanggal_absen, "%Y-%m-%d").date()
        stmt = stmt.where(Absensi.tanggal_absen == tanggal_absen)
        stmt_count = stmt_count.filter(Absensi.tanggal_absen == tanggal_absen)
    if jam_masuk or jam_keluar is not None:
        if jam_masuk:
            jam_masuk = datetime.strptime(jam_masuk, "%H:%M:%S").time()
            stmt = stmt.where(Absensi.jam_masuk == jam_masuk)
            stmt_count = stmt_count.filter(Absensi.jam_masuk == jam_masuk)
        if jam_keluar:
            jam_keluar = datetime.strptime(jam_keluar, "%H:%M:%S").time()
            stmt = stmt.where(Absensi.jam_keluar == jam_keluar)
            stmt_count = stmt_count.filter(Absensi.jam_keluar == jam_keluar)
    stmt = stmt.order_by(Absensi.id.asc()).limit(limit=limit).offset(offset=offset)
    get_list = db.execute(stmt).scalars().all()
    num_data = db.execute(stmt_count).scalar()
    num_page = ceil(num_data / limit)
    return get_list, num_data, num_page

def get_by_id(
    db: Session,
    id: int,
) -> Absensi:
    query = select(Absensi).filter(Absensi.id == id)
    data = db.execute(query).scalar()
    return data

def create(
    db: Session,
    keterangan: str,
    lokasi: str,
    userId: User,
    shiftId: Shift,
    kehadiranId: Kehadiran,
    is_commit: bool = True
) -> Absensi:
    new_data = Absensi(
        tanggal_absen=datetime.today().date(),
        jam_masuk=datetime.today().strftime("%H:%M:%S"),
        keterangan=keterangan,
        lokasi=lokasi,
        absen_user=userId,
        absen_shift=shiftId,
        absen_kehadiran=kehadiranId
    )
    db.add(new_data)
    if is_commit:
        db.commit()
    return new_data

def update_exit_time(
    db: Session,
    id: int,
    is_commit: bool = True
) -> Optional[Absensi]:
    query = select(Absensi).filter(
        Absensi.id == id, 
        Absensi.jam_keluar == None #NOQA
    )
    data = db.execute(query).scalar()
    if data is None:
        return None
    data.jam_keluar = datetime.today().strftime("%H:%M:%S")
    db.add(data)
    if is_commit:
        db.commit()
    return data