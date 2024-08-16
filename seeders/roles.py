from sqlalchemy.orm import Session
from migrations.factories.RoleFactory import RoleFactory

list_role = {"Admin", "Operator", "Guru", "Karyawan"}


def initial_role(db: Session, is_commit: bool = True):
    for data in list_role:
        role = RoleFactory.create(jabatan=data)
        db.add(role)
    if is_commit:
        db.commit()
    return True
