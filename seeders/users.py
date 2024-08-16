from sqlalchemy.orm import Session
from common.security import generate_hash_password
from models.User import User
from models.Role import Role
from migrations.factories.UserFactory import UserFactory

def initial_user(
    db: Session,
    is_commit: bool = True
) -> User:
    role = (db.query(Role).filter(Role.jabatan == "Admin").first())
    user = UserFactory.create(
        nama="Admin",
        email="admin@absensi.py",
        password=generate_hash_password("12qwaszx"),
        userRole=role
    )
    db.add(user)
    if is_commit:
        db.commit()
    return user