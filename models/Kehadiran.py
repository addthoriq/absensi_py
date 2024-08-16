from . import Base
from sqlalchemy import Column, Integer, String, VARCHAR


class Kehadiran(Base):
    __tablename__ = "kehadiran"

    id = Column("id", Integer, nullable=False, autoincrement=True, primary_key=True)
    nama_kehadiran = Column("nama_kehadiran", String(50))
    keterangan = Column("keterangan", VARCHAR(100))
