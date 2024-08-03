from . import Base
from sqlalchemy import Column, Integer, VARCHAR, Time

class Shift(Base):
    __tablename__ = "shift"

    id = Column("id", Integer, primary_key=True, nullable=False, autoincrement=True)
    nama_shift = Column("nama_shift", VARCHAR(50))
    jam_mulai = Column("jam_mulai_shift", Time)
    jam_akhir = Column("jam_berakhir_shift", Time)