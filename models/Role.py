from . import Base
from sqlalchemy import Column, Integer, String


class Role(Base):
    __tablename__ = "role"

    id = Column("id", Integer, primary_key=True, nullable=False, autoincrement=True)
    jabatan = Column("nama_role", String(100))
