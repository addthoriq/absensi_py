from sqlalchemy.orm import Session
from models.User import User
from models.Role import Role
from sqlalchemy import select, func
from typing import List, Optional, Tuple
from math import ceil
from common.security import generate_hash_password


def list_users(
    db: Session,
    page: int = 1,
    page_size: int = 10,
    nama: Optional[str] = None,
    email: Optional[str] = None,
    jabatan: Optional[int] = None,
) -> Tuple[List[User], int, int]:
    limit = page_size
    offset = (page - 1) * limit
    stmt = select(User)
    stmt_count = select(func.count(User.id))
    if nama is not None:
        stmt = stmt.filter(User.nama.ilike(f"%{nama}%"))
        stmt_count = stmt_count.filter(User.nama.ilike(f"%{nama}%"))
    if email is not None:
        stmt = stmt.filter(User.email.ilike(f"%{email}%"))
        stmt_count = stmt_count.filter(User.email.ilike(f"%{email}%"))
    if jabatan is not None:
        stmt = stmt.filter(User.role_id == jabatan)
        stmt_count = stmt_count.filter(User.role_id == jabatan)
    stmt = stmt.order_by(User.id.asc()).limit(limit=limit).offset(offset=offset)
    get_list = db.execute(stmt).scalars().all()
    num_data = db.execute(stmt_count).scalar()
    num_page = ceil(num_data / limit)
    return get_list, num_data, num_page


def get_user_by_id(db: Session, id: int) -> User:
    query = select(User).filter(User.id == id).join(Role, User.role_id == Role.id)
    return db.execute(query).scalar()


def create_user(
    db: Session,
    nama: str,
    email: str,
    password: str,
    jabatan: int,
    is_commit: bool = True,
) -> User:
    new_user = User(
        nama=nama,
        email=email,
        password=generate_hash_password(password),
        role_id=jabatan,
    )
    db.add(new_user)
    if is_commit:
        db.commit()
    return new_user


def update_user(
    db: Session, id: int, nama: str, email: str, jabatan: int, is_commit: bool = True
) -> User:
    query = select(User).filter(User.id == id)
    data = db.execute(query).scalar()
    data.nama = nama
    data.email = email
    data.role_id = jabatan
    db.add(data)
    if is_commit:
        db.commit()
    return data


def delete_user(db: Session, id: int, is_commit: bool = True) -> None:
    query = db.query(User).filter(User.id == id).first()
    db.delete(query)
    if is_commit:
        db.commit()
    return None
